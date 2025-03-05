import time
from typing import Any, Dict, List, Optional

from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.connections.data_types import RESTMethod, RESTRequest
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory


def build_api_factory(
    throttler,
    time_synchronizer: TimeSynchronizer,
    auth: Optional[Any] = None,
) -> WebAssistantsFactory:
    return WebAssistantsFactory(
        throttler=throttler,
        time_synchronizer=time_synchronizer,
        auth=auth,
    )

def rest_encode_params(params: Dict[str, Any]) -> str:
    return "&".join([f"{key}={value}" for key, value in params.items()])

def get_timestamp() -> int:
    return int(time.time() * 1000)

def convert_from_exchange_trading_pair(trading_pair: str) -> str:
    return trading_pair.replace("_", "-")

def convert_to_exchange_trading_pair(trading_pair: str) -> str:
    return trading_pair.replace("-", "_")

def get_new_client_order_id(is_buy: bool, trading_pair: str) -> str:
    side = "B" if is_buy else "S"
    return f"{side}-{trading_pair}-{int(time.time() * 1e6)}"

def create_throttler(trading_pairs: List[str]) -> Any:
    # TODO: Implement proper rate limits based on trading pairs
    from hummingbot.core.api_throttler.async_throttler import AsyncThrottler
    return AsyncThrottler(rate_limits=[])

def validate_response(response: Dict[str, Any]) -> bool:
    if "result" in response:
        return response["result"] == "true"
    return False

def extract_order_id(response: Dict[str, Any]) -> Optional[str]:
    return response.get("id")

def extract_trade_id(response: Dict[str, Any]) -> Optional[str]:
    return response.get("trade_id")

def extract_order_status(response: Dict[str, Any]) -> Optional[str]:
    return response.get("status")

def extract_order_filled_amount(response: Dict[str, Any]) -> float:
    return float(response.get("filled_amount", 0.0))

def extract_order_remaining_amount(response: Dict[str, Any]) -> float:
    return float(response.get("remaining_amount", 0.0))
