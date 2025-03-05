import json
from typing import Any, Dict, Optional
from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTRequest, WSRequest
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory
from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_auth import GateIoDeliveryAuth

def build_api_factory(
    auth: Optional[GateIoDeliveryAuth] = None,
    time_synchronizer: Optional[TimeSynchronizer] = None,
) -> WebAssistantsFactory:
    return WebAssistantsFactory(
        auth=auth,
        time_synchronizer=time_synchronizer,
    )

def rest_url(path_url: str, domain: str = "api") -> str:
    base_url = f"https://{domain}.gateio.ws/api/v4"
    return base_url + path_url

def wss_url(path_url: str, domain: str = "api") -> str:
    base_url = f"wss://{domain}.gateio.ws/ws/v4/"
    return base_url + path_url

def build_api_factory_without_time_synchronizer_pre_processor(
    auth: Optional[GateIoDeliveryAuth] = None,
) -> WebAssistantsFactory:
    return WebAssistantsFactory(auth=auth)

def create_throttler() -> Dict[str, Any]:
    return {
        "public": {
            "limit_id": "public",
            "limit": 10,
            "time_interval": 1,
            "weight": 1,
        },
        "private": {
            "limit_id": "private",
            "limit": 5,
            "time_interval": 1,
            "weight": 1,
        },
        "ws_auth": {
            "limit_id": "ws_auth",
            "limit": 10,
            "time_interval": 1,
            "weight": 1,
        },
    }

def is_exchange_information_valid(exchange_info: Dict[str, Any]) -> bool:
    return (
        exchange_info is not None
        and "status" in exchange_info
        and exchange_info["status"] == "ok"
    )
