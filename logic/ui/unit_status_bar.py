from logic.core.draw_queue import DrawQueue
from logic.core.lifecycle import Lifecycle
from logic.core.lifecycle_group import LifecycleGroup
from logic.core.render.component import Component
from logic.core.render.components.hstack import HStack
from logic.core.render.components.rect import Rect
from logic.core.render.components.zstack import ZStack, ZStackAlignment
from logic.ui.colors import Colors
from logic.entities.units.brains.unit_brain import Unit
from logic.entities.units.data.unit_metadata import UnitMetadataKey


class UnitStatusBar(Lifecycle):
    def __init__(self,
                 group: LifecycleGroup,
                 unit: Unit,
                 offset: tuple[float, float]):
        super().__init__(group=group)
        self.__unit = unit
        self.__x_offset, self.__y_offset = offset

    def render(self, queue: DrawQueue):
        should_show = False
        if UnitMetadataKey.DAMAGE_TAKEN in self.__unit.metadata:
            should_show = self.__unit.metadata[UnitMetadataKey.DAMAGE_TAKEN]
        if should_show:
            original_souls = self.__unit.metadata[UnitMetadataKey.ORIGINAL_SOULS]
            original_armor = self.__unit.metadata[UnitMetadataKey.ORIGINAL_ARMOR]
            hp_percent = int(10 * min(1, self.__unit.souls / original_souls)) / 10
            armor_percent = int(10 * min(1, self.__unit.armor / max(original_souls, original_armor))) / 10
            HStack(
                children=[
                    ZStack(
                        children=[
                            Rect(
                                size=(24, 6),
                                color=Colors.BLACK,
                                border=(2, Colors.BLACK),
                                border_radius=3
                            ),
                            Rect(
                                size=(24 * hp_percent, 6),
                                color=Colors.RED,
                                border=(2, Colors.BLACK),
                                border_radius=3
                            ),
                            Rect(
                                size=(24 * armor_percent, 6),
                                color=Colors.GRAY,
                                border=(2, Colors.BLACK),
                                border_radius=3
                            )
                        ],
                        alignment=ZStackAlignment.CENTER_LEFT
                    )
                ] + self.__effect_components(),
                spacing=8
            ).draw(
                position=(self.__unit.position.x + self.__x_offset, self.__unit.position.y + self.__y_offset),
                queue=queue,
                game_space=True,
                priority=1
            )

    def __effect_components(self) -> list[Component]:
        components = []
        for effect in self.__unit.effects:
            component = effect.status_bar_component(size=(16, 16))
            if component is not None:
                components.append(component)
        return components
