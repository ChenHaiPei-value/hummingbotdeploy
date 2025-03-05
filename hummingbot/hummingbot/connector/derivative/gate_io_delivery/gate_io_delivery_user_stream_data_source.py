import asyncio
import logging
from typing import Any, AsyncIterable, Dict, Optional

from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_auth import GateIoDeliveryAuth
from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_web_utils import build_api_factory
from hummingbot.core.api_throttler.async_throttler import AsyncThrottler
from hummingbot.core.data_type.user_stream_tracker_data_source import UserStreamTrackerDataSource
from hummingbot.core.web_assistant.connections.data_types import WSJSONRequest
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory
from hummingbot.core.web_assistant.ws_assistant import WSAssistant
from hummingbot.logger import HummingbotLogger


class GateIoDeliveryUserStreamDataSource(UserStreamTrackerDataSource):
    _logger: Optional[HummingbotLogger] = None

    @classmethod
    def logger(cls) -> HummingbotLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def __init__(self, auth: GateIoDeliveryAuth, throttler: AsyncThrottler, api_factory: WebAssistantsFactory):
        super().__init__()
        self._auth = auth
        self._throttler = throttler
        self._api_factory = api_factory
        self._ws_assistant: Optional[WSAssistant] = None

    @property
    def last_recv_time(self) -> float:
        if self._ws_assistant:
            return self._ws_assistant.last_recv_time
        return 0

    async def listen_for_user_stream(self, output: asyncio.Queue) -> AsyncIterable[Any]:
        """
        Connects to the user private channel in the exchange and listens to all balance and order updates.
        """
        while True:
            try:
                self._ws_assistant = await self._api_factory.get_ws_assistant()
                await self._ws_assistant.connect(ws_url="wss://api.gateio.ws/ws/v4/")
                await self._ws_assistant.subscribe(WSJSONRequest(payload={
                    "time": int(self._auth.time_provider.time() * 1000),
                    "channel": "futures.orders",
                    "event": "subscribe",
                    "payload": []
                }))
                await self._ws_assistant.subscribe(WSJSONRequest(payload={
                    "time": int(self._auth.time_provider.time() * 1000),
                    "channel": "futures.balances",
                    "event": "subscribe",
                    "payload": []
                }))

                async for ws_response in self._ws_assistant.iter_messages():
                    data = ws_response.data
                    if "error" in data:
                        self.logger().error(f"WebSocket error: {data['error']}")
                        continue
                    output.put_nowait(data)

            except asyncio.CancelledError:
                raise
            except Exception:
                self.logger().error("Unexpected error with Gate.io WebSocket connection. Retrying after 30 seconds...",
                                   exc_info=True)
                await asyncio.sleep(30.0)
