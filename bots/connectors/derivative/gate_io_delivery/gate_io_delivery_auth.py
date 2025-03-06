import hmac
import hashlib
import time
from typing import Dict, Any

class GateIoDeliveryAuth:
    """
    Auth class required by Gate.io Delivery API
    """

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    def generate_auth_dict(
        self, 
        method: str, 
        path: str, 
        params: Dict[str, Any] = None, 
        body: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generates authentication headers for Gate.io Delivery API
        """
        timestamp = str(int(time.time()))
        message = f"{timestamp}\n{method}\n{path}\n"

        if params:
            message += f"{self._format_params(params)}\n"
        else:
            message += "\n"

        if body:
            message += f"{self._format_body(body)}\n"
        else:
            message += "\n"

        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha512
        ).hexdigest()

        return {
            "KEY": self.api_key,
            "Timestamp": timestamp,
            "SIGN": signature,
        }

    def _format_params(self, params: Dict[str, Any]) -> str:
        """
        Formats query parameters for signature generation
        """
        return "&".join(f"{k}={v}" for k, v in sorted(params.items()))

    def _format_body(self, body: Dict[str, Any]) -> str:
        """
        Formats request body for signature generation
        """
        return "&".join(f"{k}={v}" for k, v in sorted(body.items()))
