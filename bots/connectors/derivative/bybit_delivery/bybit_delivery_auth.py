import hmac
import hashlib
import time
from urllib.parse import urlencode
from bots.connectors.derivative.base_auth import APIAuthBase

class BybitDeliveryAuth(APIAuthBase):
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.recv_window = 5000  # 根据Bybit推荐设置

    def generate_signature(self, params: dict) -> str:
        """生成Bybit V5签名"""
        timestamp = int(time.time() * 1000)
        params.update({
            "api_key": self.api_key,
            "timestamp": timestamp,
            "recv_window": self.recv_window
        })
        
        # 按参数名排序
        param_str = urlencode(sorted(params.items()))
        # 使用SHA256哈希
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            param_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        params["sign"] = signature
        return timestamp

    def add_auth_to_params(self, params: dict) -> dict:
        timestamp = self.generate_signature(params)
        return params

    def add_auth_to_headers(self, headers: dict) -> dict:
        headers["X-BAPI-API-KEY"] = self.api_key
        headers["X-BAPI-TIMESTAMP"] = str(int(time.time() * 1000))
        headers["X-BAPI-RECV-WINDOW"] = str(self.recv_window)
        return headers

    def get_ws_auth_params(self) -> dict:
        expires = int(time.time() * 1000) + 1000
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            f"GET/realtime{expires}".encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return {
            "api_key": self.api_key,
            "expires": expires,
            "signature": signature
        }
