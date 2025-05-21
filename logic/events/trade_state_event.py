from enum import Enum

from logic.events.event import Event


class TradeState(Enum):
    BUY = 'buy'
    SELL = 'sell'
    NONE = 'none'


class TradeStateEvent(Event):
    def __init__(self, state: TradeState, can_trade_now: bool = False):
        self.state = state
        self.can_trade_now = can_trade_now
