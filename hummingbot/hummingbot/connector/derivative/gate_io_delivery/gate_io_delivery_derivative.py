from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_auth import GateIoDeliveryAuth
from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_web_utils import (
    build_api_factory,
    create_throttler,
    rest_url,
    wss_url,
)
from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_constants import (
    ORDER_TYPES,
    TRADE_TYPES,
    TIME_IN_FORCE,
    ORDER_STATUS_OPEN,
    ORDER_STATUS_CLOSED,
    ORDER_STATUS_CANCELLED,
    POSITION_STATUS_OPEN,
    POSITION_STATUS_CLOSED,
)
from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_order_book_tracker import GateIoDeliveryOrderBookTracker
from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_user_stream_data_source import (
    GateIoDeliveryUserStreamDataSource,
)
from hummingbot.connector.derivative.gate_io_delivery.gate_io_delivery_utils import (
    convert_from_exchange_trading_pair,
    convert_to_exchange_trading_pair,
)
from hummingbot.connector.derivative_base import DerivativeBase
from hummingbot.core.data_type.common import OrderType, TradeType
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.trade_fee import TradeFeeBase
from hummingbot.core.event.events import (
    MarketEvent,
    OrderFilledEvent,
    OrderCancelledEvent,
    OrderType,
    TradeType,
)
from hummingbot.core.network_iterator import NetworkStatus
from hummingbot.core.utils.async_utils import safe_ensure_future
from hummingbot.core.api_throttler.async_throttler import AsyncThrottler
from hummingbot.core.api_throttler.data_types import RateLimit
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory
from hummingbot.core.web_assistant.connections.data_types import RESTRequest


class GateIoDeliveryDerivative(DerivativeBase):
    """
    Gate.io Delivery Connector
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        trading_pairs: Optional[List[str]] = None,
        trading_required: bool = True,
    ):
        self._api_key = api_key
        self._secret_key = secret_key
        self._trading_pairs = trading_pairs
        self._trading_required = trading_required
        self._auth = GateIoDeliveryAuth(api_key=self._api_key, secret_key=self._secret_key)
        self._throttler = AsyncThrottler(rate_limits=[
            RateLimit(limit_id="rest_api", limit=300, time_interval=1),
            RateLimit(limit_id="ws_auth", limit=10, time_interval=1),
            RateLimit(limit_id="ws_public", limit=20, time_interval=1),
        ])
        self._api_factory = WebAssistantsFactory(
            throttler=self._throttler,
            auth=self._auth
        )
        self._order_book_tracker = GateIoDeliveryOrderBookTracker(
            trading_pairs=self._trading_pairs,
            throttler=self._throttler,
            api_factory=self._api_factory,
        )
        self._user_stream_tracker = GateIoDeliveryUserStreamDataSource(
            auth=self._auth,
            throttler=self._throttler,
            api_factory=self._api_factory,
        )
        super().__init__()

    @property
    def name(self) -> str:
        return "gate_io_delivery"

    @property
    def order_books(self) -> Dict[str, OrderBook]:
        return self._order_book_tracker.order_books

    @property
    def trading_rules(self) -> Dict[str, Any]:
        return self._order_book_tracker.trading_rules

    @property
    def in_flight_orders(self) -> Dict[str, Any]:
        return self._order_book_tracker.in_flight_orders

    @property
    def status_dict(self) -> Dict[str, bool]:
        return {
            "order_books_initialized": self._order_book_tracker.ready,
            "account_balance": len(self._account_balances) > 0,
            "trading_required": self._trading_required,
        }

    @property
    def ready(self) -> bool:
        return all(self.status_dict.values())

    async def start_network(self):
        await self._order_book_tracker.start()
        if self._trading_required:
            await self._user_stream_tracker.start()

    async def stop_network(self):
        await self._order_book_tracker.stop()
        if self._trading_required:
            await self._user_stream_tracker.stop()

    async def check_network(self) -> NetworkStatus:
        try:
            await self._api_factory.get_rest_assistant().execute_request(
                RESTRequest(method="GET", url=rest_url("/futures/contracts"))
            )
            return NetworkStatus.CONNECTED
        except Exception:
            return NetworkStatus.NOT_CONNECTED

    async def get_order_status(self, client_order_id: str) -> Dict[str, Any]:
        return await self._order_book_tracker.get_order_status(client_order_id)

    async def get_trading_fees(self) -> Dict[str, Any]:
        return await self._order_book_tracker.get_trading_fees()

    async def get_account_balances(self) -> Dict[str, Decimal]:
        return await self._order_book_tracker.get_account_balances()

    async def place_order(
        self,
        trading_pair: str,
        amount: Decimal,
        is_buy: bool,
        order_type: OrderType,
        price: Decimal,
    ) -> str:
        return await self._order_book_tracker.place_order(
            trading_pair=trading_pair,
            amount=amount,
            is_buy=is_buy,
            order_type=order_type,
            price=price,
        )

    async def cancel_order(self, client_order_id: str) -> bool:
        return await self._order_book_tracker.cancel_order(client_order_id)

    async def get_open_orders(self) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_open_orders()

    async def get_order_book(self, trading_pair: str) -> OrderBook:
        return await self._order_book_tracker.get_order_book(trading_pair)

    async def get_trades(self, trading_pair: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_trades(trading_pair)

    async def get_balances(self) -> Dict[str, Decimal]:
        return await self._order_book_tracker.get_balances()

    async def get_position(self, trading_pair: str) -> Dict[str, Any]:
        return await self._order_book_tracker.get_position(trading_pair)

    async def get_funding_info(self, trading_pair: str) -> Dict[str, Any]:
        return await self._order_book_tracker.get_funding_info(trading_pair)

    async def get_funding_payment(self, trading_pair: str) -> Dict[str, Any]:
        return await self._order_book_tracker.get_funding_payment(trading_pair)

    async def get_funding_rate(self, trading_pair: str) -> Dict[str, Any]:
        return await self._order_book_tracker.get_funding_rate(trading_pair)

    async def get_funding_rate_history(self, trading_pair: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_history(trading_pair)

    async def get_funding_payment_history(self, trading_pair: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_payment_history(trading_pair)

    async def get_funding_rate_prediction(self, trading_pair: str) -> Dict[str, Any]:
        return await self._order_book_tracker.get_funding_rate_prediction(trading_pair)

    async def get_funding_rate_prediction_history(self, trading_pair: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_history(trading_pair)

    async def get_funding_rate_prediction_accuracy(self, trading_pair: str) -> Dict[str, Any]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy(trading_pair)

    async def get_funding_rate_prediction_accuracy_history(self, trading_pair: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_history(trading_pair)

    async def get_funding_rate_prediction_accuracy_summary(self, trading_pair: str) -> Dict[str, Any]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary(trading_pair)

    async def get_funding_rate_prediction_accuracy_summary_history(self, trading_pair: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_history(trading_pair)

    async def get_funding_rate_prediction_accuracy_summary_all(self) -> Dict[str, Any]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all()

    async def get_funding_rate_prediction_accuracy_summary_all_history(self) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history()

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair(self, trading_pair: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair(trading_pair)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time(self, trading_pair: str, start_time: int, end_time: int) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time(trading_pair, start_time, end_time)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval(self, trading_pair: str, start_time: int, end_time: int, interval: int) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval(trading_pair, start_time, end_time, interval)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit(trading_pair, start_time, end_time, interval, limit)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset(trading_pair, start_time, end_time, interval, limit, offset)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order(trading_pair, start_time, end_time, interval, limit, offset, order)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str, sort: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort(trading_pair, start_time, end_time, interval, limit, offset, order, sort)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str, sort: str, filter: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter(trading_pair, start_time, end_time, interval, limit, offset, order, sort, filter)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str, sort: str, filter: str, group: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group(trading_pair, start_time, end_time, interval, limit, offset, order, sort, filter, group)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str, sort: str, filter: str, group: str, having: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having(trading_pair, start_time, end_time, interval, limit, offset, order, sort, filter, group, having)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str, sort: str, filter: str, group: str, having: str, select: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select(trading_pair, start_time, end_time, interval, limit, offset, order, sort, filter, group, having, select)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select_and_from(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str, sort: str, filter: str, group: str, having: str, select: str, from_: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select_and_from(trading_pair, start_time, end_time, interval, limit, offset, order, sort, filter, group, having, select, from_)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select_and_from_and_where(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str, sort: str, filter: str, group: str, having: str, select: str, from_: str, where: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select_and_from_and_where(trading_pair, start_time, end_time, interval, limit, offset, order, sort, filter, group, having, select, from_, where)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select_and_from_and_where_and_group_by(self, trading_pair: str, start_time: int, end_time: int, interval: int, limit: int, offset: int, order: str, sort: str, filter: str, group: str, having: str, select: str, from_: str, where: str, group_by: str) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select_and_from_and_where_and_group_by(trading_pair, start_time, end_time, interval, limit, offset, order, sort, filter, group, having, select, from_, where, group_by)

    async def get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select_and_from_and_where_and_group_by_and_having(
        self,
        trading_pair: str,
        start_time: int,
        end_time: int,
        interval: int,
        limit: int,
        offset: int,
        order: str,
        sort: str,
        filter: str,
        group: str,
        having: str,
        select: str,
        from_: str,
        where: str,
        group_by: str,
    ) -> List[Dict[str, Any]]:
        return await self._order_book_tracker.get_funding_rate_prediction_accuracy_summary_all_history_by_trading_pair_and_time_and_interval_and_limit_and_offset_and_order_and_sort_and_filter_and_group_and_having_and_select_and_from_and_where_and_group_by_and_having(
            trading_pair=trading_pair,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            limit=limit,
            offset=offset,
            order=order,
            sort=sort,
            filter=filter,
            group=group,
            having=having,
            select=select,
            from_=from_,
            where=where,
            group_by=group_by,
        )
