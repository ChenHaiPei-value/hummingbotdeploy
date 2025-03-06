from typing import Dict, List, Optional
from decimal import Decimal
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

from hummingbot.core.data_type.common import TradeType, OrderType, PositionAction
from hummingbot.core.data_type.in_flight_order import InFlightOrder
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.trade_fee import TradeFeeSchema

from bots.connectors.derivative.binance_futures.binance_futures_auth import BinanceFuturesAuth

from ..base_derivative import BaseDerivative
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.event.events import OrderType

class BinanceFuturesDerivative(BaseDerivative):
    async def get_funding_rate(self) -> float:
        """实现资金费率获取逻辑"""
        data = await self._api_request("GET", "/fapi/v1/premiumIndex")
        return float(data["lastFundingRate"])

    async def create_order(self, order_type: OrderType, price: float, amount: float):
        """实现标准化的订单创建接口"""
        # 转换订单类型到Binance特定类型
        binance_order_type = "LIMIT" if order_type == OrderType.LIMIT else "MARKET"
        response = await self._api_request(
            "POST", "/fapi/v1/order",
            data={
                "symbol": self.symbol,
                "side": "BUY" if amount > 0 else "SELL",
                "type": binance_order_type,
                "quantity": abs(amount),
                "price": str(price),
                "timeInForce": "GTC"
            }
        )
        return self._parse_order_response(response)

    async def update_order_book(self):
        """从交易所获取最新订单簿数据"""
        depth_data = await self._api_request("GET", "/fapi/v1/depth", params={
            "symbol": self.symbol,
            "limit": 100
        })
        self._order_book.apply_snapshot({
            "bids": [(entry[0], entry[1]) for entry in depth_data["bids"]],
            "asks": [(entry[0], entry[1]) for entry in depth_data["asks"]],
            "update_id": depth_data["lastUpdateId"]
        })
    BASE_URL = "https://fapi.binance.com"
    
    def __init__(self, auth: BinanceFuturesAuth):
        super().__init__(auth)
        self.symbol = "BTC-USDT"  # 示例交易对，实际应从配置读取
        
    def get_fee(self,
               base_currency: str,
               quote_currency: str,
               order_type: OrderType,
               order_side: TradeType,
               amount: float,
               price: float,
               is_maker: bool) -> TradeFeeSchema:
        """Get fee schema for Binance Futures"""
        return TradeFeeSchema(
            percent=0.0002 if is_maker else 0.0004,
            flat_fees=[]
        )
        
    def get_order_book(self, trading_pair: str) -> OrderBook:
        """Get order book for trading pair"""
        endpoint = "/fapi/v1/depth"
        params = {
            "symbol": trading_pair.replace("-", ""),
            "limit": 100
        }
        response = self._signed_request("GET", endpoint, params)
        return self._parse_order_book(response)
        
    def _signed_request(self, method: str, endpoint: str, params: dict = None) -> dict:
        """Make signed API request"""
        if params is None:
            params = {}
            
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.auth.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        params["signature"] = signature
        headers = {
            "X-MBX-APIKEY": self.auth.api_key
        }
        
        response = requests.request(
            method,
            self.BASE_URL + endpoint,
            params=params,
            headers=headers
        )
        return response.json()
        
    def _parse_order_book(self, data: dict) -> OrderBook:
        """Parse order book response"""
        bids = [(Decimal(price), Decimal(amount)) for price, amount in data['bids']]
        asks = [(Decimal(price), Decimal(amount)) for price, amount in data['asks']]
        self._order_book.apply_snapshot(bids, asks, data['lastUpdateId'])
        return self._order_book
