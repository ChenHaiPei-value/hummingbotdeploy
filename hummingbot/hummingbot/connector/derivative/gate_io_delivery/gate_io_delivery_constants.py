from enum import Enum

REST_URL = "https://api.gateio.ws/api/v4"
WS_URL = "wss://api.gateio.ws/ws/v4/"

class OrderType(Enum):
    LIMIT = "limit"
    MARKET = "market"

class TradeType(Enum):
    BUY = "buy"
    SELL = "sell"

class TimeInForce(Enum):
    GTC = "gtc"
    IOC = "ioc"
    FOK = "fok"

ORDER_TYPES = [OrderType.LIMIT.value, OrderType.MARKET.value]
TRADE_TYPES = [TradeType.BUY.value, TradeType.SELL.value]
TIME_IN_FORCE = [TimeInForce.GTC.value, TimeInForce.IOC.value, TimeInForce.FOK.value]

ORDER_STATUS_OPEN = "open"
ORDER_STATUS_CLOSED = "closed"
ORDER_STATUS_CANCELLED = "cancelled"

POSITION_STATUS_OPEN = "open"
POSITION_STATUS_CLOSED = "closed"

RATE_LIMITS = [
    {
        "limit_id": "public",
        "limit": 10,
        "time_interval": 1,
        "weight": 1,
    },
    {
        "limit_id": "private",
        "limit": 5,
        "time_interval": 1,
        "weight": 1,
    },
    {
        "limit_id": "ws_auth",
        "limit": 10,
        "time_interval": 1,
        "weight": 1,
    },
]
