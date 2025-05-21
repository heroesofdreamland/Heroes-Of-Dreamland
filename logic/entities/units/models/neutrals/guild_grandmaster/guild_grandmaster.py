from pymunk import Circle, Body, Vec2d
from logic.core.lifecycle_group import LifecycleGroup
from logic.entities.enemies_provider import EnemiesProvider
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.models.neutrals.guild_grandmaster.guild_grandmaster_animation_model import GuildGrandmasterAnimationModel


class GuildGrandmaster(Unit):
    def __init__(self,
                 identifier: str,
                 group: LifecycleGroup,
                 x: float,
                 y: float,
                 enemies_provider: EnemiesProvider,
                 config: dict | None = None):

        animation_model = GuildGrandmasterAnimationModel()
        shape = Circle(body=Body(body_type=Body.KINEMATIC), radius=24)

        super().__init__(identifier=identifier,
                         position=Vec2d(x, y),
                         shape=shape,
                         group=group,
                         animation_model=animation_model,
                         animated_object=animation_model.build_animated_object(scale=1, offset=(-36, -36)),
                         speed=0,
                         attack_config=None,
                         souls=1,
                         armor=0,
                         abilities=[],
                         reward=None,
                         enemies_provider=lambda: [],
                         name='Origin trader')