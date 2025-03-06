from typing import Dict, List
import aiohttp
from bots.connectors.derivative.base_derivative import BaseDerivative
from .bybit_delivery_auth import BybitDeliveryAuth

class BybitDeliveryDerivative(BaseDerivative):
    def __init__(self, auth: BybitDeliveryAuth):
        super().__init__()
        self.auth = auth
        self.base_url = "https://api.bybit.com"
        self.ws_url = "wss://stream.bybit.com/v5/public/linear"
        self.session = aiohttp.ClientSession()

    async def get_order_book(self, symbol: str) -> Dict:
        """获取合约订单簿"""
        endpoint = "/v5/market/orderbook"
        params = {"category": "linear", "symbol": symbol}
        return await self._api_request("GET", endpoint, params=params)

    async def get_balance(self) -> Dict:
        """获取合约账户余额"""
        endpoint = "/v5/account/wallet-balance"
        params = {"accountType": "CONTRACT"}
        return await self._api_request("GET", endpoint, params=params)

    async def place_order(self, 
                        symbol: str,
                        side: str,
                        order_type: str,
                        qty: float,
                        price: float = None,
                        time_in_force: str = "GoodTillCancel") -> Dict:
        """创建合约订单"""
        endpoint = "/v5/order/create"
        data = {
            "category": "linear",
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "qty": str(qty),
            "timeInForce": time_in_force
        }
        if price:
            data["price"] = str(price)
        return await self._api_request("POST", endpoint, data=data)

    async def _api_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """处理API请求"""
        headers = {"Content-Type": "application/json"}
        headers = self.auth.add_auth_to_headers(headers)
        
        try:
            if method == "GET":
                params = kwargs.get("params", {})
                params = self.auth.add_auth_to_params(params)
                async with self.session.get(f"{self.base_url}{endpoint}", 
                                          params=params, 
                                          headers=headers) as response:
                    return await self._handle_response(response)
            else:
                data = kwargs.get("data", {})
                data = self.auth.add_auth_to_params(data)
                async with self.session.post(f"{self.base_url}{endpoint}", 
                                           json=data,
                                           headers=headers) as response:
                    return await self._handle_response(response)
        except Exception as e:
            return {"error": str(e)}

    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict:
        """统一处理响应"""
        if response.status == 200:
            return await response.json()
        else:
            error_msg = await response.text()
            return {
                "error": f"API request failed ({response.status})",
                "details": error_msg
            }

    async def close(self):
        """关闭会话"""
        await self.session.close()
