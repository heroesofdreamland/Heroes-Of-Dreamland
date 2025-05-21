class LifecycleGroupIndex:
    def __init__(self,
                 index: int,
                 sort_by_coordinate: bool = False):
        self.index = index
        self.sort_by_coordinate = sort_by_coordinate


class LifecycleGroup:
    def __init__(self, index: LifecycleGroupIndex):
        self.index = index

        self.__disable_input_reasons = set()
        self.__disable_update_reasons = set()
        self.__disable_render_reasons = set()
        self.__disable_animation_reasons = set()

        self.__timers: list = []

    @property
    def is_input_enabled(self) -> bool:
        return not self.__disable_input_reasons

    @property
    def is_update_enabled(self) -> bool:
        return not self.__disable_update_reasons

    @property
    def is_render_enabled(self) -> bool:
        return not self.__disable_render_reasons

    @property
    def is_animation_enabled(self) -> bool:
        return not self.__disable_animation_reasons

    def reset(self):
        self.__disable_input_reasons = set()
        self.__disable_update_reasons = set()
        self.__disable_render_reasons = set()
        self.__disable_animation_reasons = set()

    def set_input_enabled(self, is_enabled: bool, reason: str):
        if is_enabled:
            self.__disable_input_reasons.discard(reason)
        else:
            self.__disable_input_reasons.add(reason)

    def set_update_enabled(self, is_enabled: bool, reason: str):
        if is_enabled:
            self.__disable_update_reasons.discard(reason)
        else:
            self.__disable_update_reasons.add(reason)
        for timer in self.__timers:
            timer.pause(is_paused=not is_enabled)

    def set_render_enabled(self, is_enabled: bool, reason: str):
        if is_enabled:
            self.__disable_render_reasons.discard(reason)
        else:
            self.__disable_render_reasons.add(reason)

    def set_animation_enabled(self, is_enabled: bool, reason: str):
        if is_enabled:
            self.__disable_animation_reasons.discard(reason)
        else:
            self.__disable_animation_reasons.add(reason)

    def register_timer(self, timer):
        self.__timers.append(timer)

    def unregister_timer(self, timer):
        self.__timers.remove(timer)
