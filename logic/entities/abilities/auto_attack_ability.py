from typing import cast, Type

from pymunk import Vec2d

from logic.entities.abilities.ability import Ability
from logic.entities.abilities.move_with_closest_enemy_ability import MoveWithClosestEnemyAbility, UnitMovementFSM
from logic.core.draw_queue import DrawQueue
from logic.core.timer import Timer
from logic.environment.environment import Groups, Environment
from logic.events.enemy_summon_event import EnemySummonEvent
from logic.ui.colors import Colors
from logic.settings.debug_settings import DebugSettings
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.helpers.unit_distances_helper import UnitDistancesHelper
from logic.entities.units.brains.mixins.unit_attack_mixin import AttackState
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.damage_data import DamageData
from logic.entities.units.data.enemy_config import EnemyConfigKey
from logic.entities.units.unit_factory import generate_unit


class __AutoAttackAbility(Ability):
    def __init__(self, trigger_radius: float, damage_radius: float, required_visibility_radius: float, enemies_provider: EnemiesProvider):
        self.__trigger_radius = trigger_radius
        self.__damage_radius = damage_radius
        self.__required_visibility_radius = required_visibility_radius
        self.__enemies_provider = enemies_provider
        self.__closest_visible_enemy: Unit | None = None
        self.__closest_visible_enemy_timer = Timer(duration=0.5)
        self.__cached_movement_ability: MoveWithClosestEnemyAbility | None = None

    def update(self, owner: object):
        owner = cast(Unit, owner)
        should_start_attack = False
        should_continue_attack = False
        # Auto attacking is only possible for directly visible enemies:
        self.__update_closest_visible_enemy_on_timer(owner=owner)
        if self.__closest_visible_enemy is not None:
            closest_enemy, distance_to_closest_enemy = self.__closest_visible_enemy
            distance_to_closest_enemy -= closest_enemy.shape_radius
            # If there is a closest visible enemy, check if it's safe to attack from current position:
            should_run_away = self.__movement_state(owner=owner, owner_position=owner.position, closest_enemy=closest_enemy) == UnitMovementFSM.RETREAT
            if not should_run_away and not owner.is_stunned:
                # Start attacking only if enemy is in trigger radius:
                if distance_to_closest_enemy <= self.__trigger_radius:
                    should_start_attack = True
                # Continue attacking while enemy is in damage radius:
                if distance_to_closest_enemy <= self.__damage_radius:
                    should_continue_attack = True
        owner.update_attack_state(should_start_attack=should_start_attack, should_continue_attack=should_continue_attack)

        match owner.attack_state:
            case AttackState.ATTACK:
                if self.__closest_visible_enemy is not None:
                    closest_enemy, distance_to_closest_enemy = self.__closest_visible_enemy
                    distance_to_closest_enemy -= closest_enemy.shape_radius
                    if distance_to_closest_enemy <= self.__damage_radius:
                        self._attack(owner=owner, unit=closest_enemy)

    def _attack(self, owner: Unit, unit: Unit):
        pass

    def __movement_state(self, owner: Unit, owner_position: Vec2d, closest_enemy: Unit) -> UnitMovementFSM:
        if self.__cached_movement_ability is None:
            self.__cached_movement_ability = owner.ability(ability_type=MoveWithClosestEnemyAbility)
        if self.__cached_movement_ability is not None:
            return self.__cached_movement_ability.movement_state(owner=owner, owner_position=owner_position, closest_enemy=closest_enemy)
        else:
            return UnitMovementFSM.WAIT

    def __update_closest_visible_enemy_on_timer(self, owner: Unit):
        if not self.__closest_visible_enemy_timer.is_running():
            self.__closest_visible_enemy_timer.start(group=Groups.objects)
            return
        if self.__closest_visible_enemy_timer.is_completed():
            self.__closest_visible_enemy_timer.stop(group=Groups.objects)
            enemies = self.__enemies_provider()
            owner_position = owner.position
            visible_enemies = filter(lambda enemy: Environment.map.pathfinder.is_path_clear(start=(owner_position.x, owner_position.y), end=(enemy.position.x, enemy.position.y), radius=self.__required_visibility_radius), enemies)
            self.__closest_visible_enemy = UnitDistancesHelper.closest_unit(point=owner_position, units=visible_enemies)


class MeleeAutoAttackAbility(__AutoAttackAbility):
    def __init__(self, trigger_radius: float, damage_radius: float, damage_data: DamageData, enemies_provider: EnemiesProvider):
        self.__damage_data = damage_data
        self.__damage_radius = damage_radius
        super().__init__(trigger_radius=trigger_radius, damage_radius=damage_radius, enemies_provider=enemies_provider, required_visibility_radius=0)

    def _attack(self, owner: Unit, unit: Unit):
        unit.get_damage(damage_data=self.__damage_data, attacker=owner)

    def render(self, owner: object, queue: DrawQueue):
        if DebugSettings.debug_settings['show_unit_damage_radii']:
            owner = cast(Unit, owner)
            position = owner.position
            queue.debug_draw_circle(color=Colors.RED, radius=self.__damage_radius, position=(position.x, position.y), game_space=True)

class RangedAutoAttackAbility(__AutoAttackAbility):
    def __init__(self, trigger_radius: float, damage_radius: float, projectile_type: Type, enemies_provider: EnemiesProvider, offset: tuple[float, float]):
        self.__projectile_type = projectile_type
        self.__enemies_provider = enemies_provider
        self.__trigger_radius = trigger_radius
        self.__damage_radius = damage_radius
        self.__offset = offset
        required_visibility_radius = self.__projectile_type(0, 0, Groups.objects, lambda: []).shape_radius
        super().__init__(trigger_radius=trigger_radius, damage_radius=damage_radius, enemies_provider=enemies_provider, required_visibility_radius=required_visibility_radius)

    def _attack(self, owner: Unit, unit: Unit):
        owner_position = owner.position
        projectile = self.__projectile_type(owner_position.x,
                                            owner_position.y,
                                            Groups.objects,
                                            self.__enemies_provider)
        Environment.map.objects.append(projectile)
        projectile.launch(destination=unit.position, owner=self, animation_offset=self.__offset)

    def render(self, owner: object, queue: DrawQueue):
        if DebugSettings.debug_settings['show_unit_damage_radii']:
            owner = cast(Unit, owner)
            owner_position = owner.position
            queue.debug_draw_circle(color=Colors.YELLOW, radius=self.__trigger_radius, position=(owner_position.x, owner_position.y), game_space=True)
            queue.debug_draw_circle(color=Colors.RED, radius=self.__damage_radius, position=(owner_position.x, owner_position.y), game_space=True)


class SummonAutoAttackAbility(__AutoAttackAbility):
    def __init__(self, trigger_radius: float, summon_type: Type, enemies_provider: EnemiesProvider):
        self.__summon_type = summon_type
        super().__init__(trigger_radius=trigger_radius, damage_radius=trigger_radius, enemies_provider=enemies_provider, required_visibility_radius=0)

    def _attack(self, owner: Unit, unit: Unit):
        new_enemy = generate_unit(unit_type=self.__summon_type,
                                  coordinate=Environment.map.random_spawn_position(),
                                  config={EnemyConfigKey.IS_SUMMONED: True})
        Environment.event_manager.send(EnemySummonEvent(enemy=new_enemy))
