import asyncio
import time
from typing import Dict, List, Optional, Any

from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_web_utils import build_api_factory
from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_constants import (
    REST_ENDPOINTS,
    WS_ENDPOINTS,
    ORDER_BOOK_DEPTH,
    ORDER_BOOK_SNAPSHOT_DELAY,
    ORDER_BOOK_SNAPSHOT_INTERVAL,
    ORDER_BOOK_WS_CHANNEL
)
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.order_book_message import OrderBookMessage
from hummingbot.core.data_type.order_book_tracker_data_source import OrderBookTrackerDataSource
from hummingbot.core.web_assistant.connections.data_types import WSJSONRequest
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory
from hummingbot.core.web_assistant.ws_assistant import WSAssistant
from hummingbot.logger import HummingbotLogger


class GateIoDeliveryAPIOrderBookDataSource(OrderBookTrackerDataSource):
    _logger: Optional[HummingbotLogger] = None

    def __init__(self, trading_pairs: List[str], api_factory: WebAssistantsFactory):
        super().__init__(trading_pairs)
        self._api_factory = api_factory
        self._ws_assistant: Optional[WSAssistant] = None

    async def get_last_traded_prices(self, trading_pairs: List[str]) -> Dict[str, float]:
        pass

    async def listen_for_trades(self, ev_loop: asyncio.AbstractEventLoop, output: asyncio.Queue):
        pass

    async def listen_for_order_book_diffs(self, ev_loop: asyncio.AbstractEventLoop, output: asyncio.Queue):
        pass

    async def listen_for_order_book_snapshots(self, ev_loop: asyncio.AbstractEventLoop, output: asyncio.Queue):
        pass

    async def listen_for_subscriptions(self):
        ws: WSAssistant = await self._get_ws_assistant()
        await ws.connect(WS_ENDPOINTS["PUBLIC"])
        
        payload = {
            "time": int(time.time()),
            "channel": "futures.order_book",
            "event": "subscribe",
            "payload": self._trading_pairs
        }
        
        subscribe_request: WSJSONRequest = WSJSONRequest(payload=payload)
        await ws.send(subscribe_request)

        async for ws_response in ws.iter_messages():
            data = ws_response.data
            if "error" in data:
                self.logger().error(f"WebSocket error: {data['error']}")
                continue
                
            if data.get("event") == "update":
                await self._process_order_book_message(data)

    async def _get_ws_assistant(self) -> WSAssistant:
        if self._ws_assistant is None:
            self._ws_assistant = await self._api_factory.get_ws_assistant()
        return self._ws_assistant

    async def _process_order_book_message(self, message: Dict):
        if "result" not in message:
            return
            
        data = message["result"]
        timestamp = int(data["t"] / 1000)
        trading_pair = data["s"]
        
        if "b" in data and "a" in data:
            # This is a diff update
            bids = [(float(price), float(amount)) for price, amount in data["b"]]
            asks = [(float(price), float(amount)) for price, amount in data["a"]]
            diff_message = OrderBookMessage(
                message_type=OrderBookMessage.DIFF,
                content={
                    "trading_pair": trading_pair,
                    "update_id": timestamp,
                    "bids": bids,
                    "asks": asks
                },
                timestamp=timestamp
            )
            await self._message_queue[OrderBookMessage.DIFF].put(diff_message)
        elif "bids" in data and "asks" in data:
            # This is a snapshot
            bids = [(float(price), float(amount)) for price, amount in data["bids"]]
            asks = [(float(price), float(amount)) for price, amount in data["asks"]]
            snapshot_message = OrderBookMessage(
                message_type=OrderBookMessage.SNAPSHOT,
                content={
                    "trading_pair": trading_pair,
                    "update_id": timestamp,
                    "bids": bids,
                    "asks": asks
                },
                timestamp=timestamp
            )
            await self._message_queue[OrderBookMessage.SNAPSHOT].put(snapshot_message)

    async def _parse_trade_message(self, raw_message: Dict[str, Any], message_queue: asyncio.Queue):
        if "result" not in raw_message:
            return
            
        data = raw_message["result"]
        timestamp = int(data["t"] / 1000)
        trading_pair = data["s"]
        trade_message = OrderBookMessage(
            message_type=OrderBookMessage.TRADE,
            content={
                "trading_pair": trading_pair,
                "trade_type": "buy" if data["m"] else "sell",
                "trade_id": data["i"],
                "update_id": timestamp,
                "price": float(data["p"]),
                "amount": float(data["q"])
            },
            timestamp=timestamp
        )
        await message_queue.put(trade_message)

    async def _parse_order_book_diff_message(self, raw_message: Dict[str, Any], message_queue: asyncio.Queue):
        if "result" not in raw_message:
            return
            
        data = raw_message["result"]
        timestamp = int(data["t"] / 1000)
        trading_pair = data["s"]
        bids = [(float(price), float(amount)) for price, amount in data["b"]]
        asks = [(float(price), float(amount)) for price, amount in data["a"]]
        
        diff_message = OrderBookMessage(
            message_type=OrderBookMessage.DIFF,
            content={
                "trading_pair": trading_pair,
                "update_id": timestamp,
                "bids": bids,
                "asks": asks
            },
            timestamp=timestamp
        )
        await message_queue.put(diff_message)

    async def _parse_order_book_snapshot_message(self, raw_message: Dict[str, Any], message_queue: asyncio.Queue):
        if "result" not in raw_message:
            return
            
        data = raw_message["result"]
        timestamp = int(data["t"] / 1000)
        trading_pair = data["s"]
        bids = [(float(price), float(amount)) for price, amount in data["bids"]]
        asks = [(float(price), float(amount)) for price, amount in data["asks"]]
        
        snapshot_message = OrderBookMessage(
            message_type=OrderBookMessage.SNAPSHOT,
            content={
                "trading_pair": trading_pair,
                "update_id": timestamp,
                "bids": bids,
                "asks": asks
            },
            timestamp=timestamp
        )
        await message_queue.put(snapshot_message)
