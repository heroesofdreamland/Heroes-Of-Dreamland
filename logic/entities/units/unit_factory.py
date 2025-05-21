from enum import Enum
from typing import Type
from pymunk import Vec2d
from logic.environment.environment import Environment, Groups
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.unit_brain import Unit

__unit_counters: dict[Type, int] = {}


class UnitGroup(Enum):
    ENEMY = 'enemy'
    SUMMON = 'summon'
    NEUTRAL = 'neutral'
    PLAYER = 'player'


def generate_unit(unit_type: Type,
                  coordinate: Vec2d,
                  group: UnitGroup = UnitGroup.ENEMY,
                  config: dict | None = None) -> Unit:
    unit = __generate_unit(
        unit_type=unit_type,
        coordinate=coordinate,
        group=group,
        config=config
    )
    match group:
        case UnitGroup.ENEMY:
            Environment.map.enemies.append(unit)
        case UnitGroup.SUMMON:
            Environment.map.summons.append(unit)
        case UnitGroup.NEUTRAL:
            Environment.map.neutrals.append(unit)
        case UnitGroup.PLAYER:
            Environment.player = unit
    return unit


def __generate_unit_id(unit_type: Type) -> str:
    current_counter = 1
    if unit_type in __unit_counters:
        current_counter = __unit_counters[unit_type] + 1
    __unit_counters[unit_type] = current_counter
    return unit_type.__name__ + '_' + str(current_counter)


def __generate_unit(unit_type: Type,
                    coordinate: Vec2d,
                    group: UnitGroup,
                    config: dict | None) -> Unit:
    unit_id = __generate_unit_id(unit_type)
    enemy = unit_type(identifier=unit_id,
                      group=Groups.player if group == UnitGroup.PLAYER else Groups.objects,
                      x=coordinate[0],
                      y=coordinate[1],
                      config=config,
                      enemies_provider=__enemies_provider(group=group))
    enemy.enable_physics(enable=True)
    return enemy


def __enemies_provider(group: UnitGroup) -> EnemiesProvider:
    match group:
        case UnitGroup.ENEMY:
            return lambda: Environment.map.summons + [Environment.player]
        case UnitGroup.SUMMON | UnitGroup.PLAYER:
            return lambda: Environment.map.enemies
        case UnitGroup.NEUTRAL:
            return lambda: []
