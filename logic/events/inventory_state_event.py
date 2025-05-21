from logic.events.event import Event


class InventoryStateEvent(Event):
    def __init__(self, is_opened: bool):
        self.is_opened = is_opened
