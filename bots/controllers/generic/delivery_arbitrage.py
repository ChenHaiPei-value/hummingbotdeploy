import time
from decimal import Decimal
from typing import Dict, List, Set

import pandas as pd
from pydantic import Field, validator

from hummingbot.client.config.config_data_types import ClientFieldData
from hummingbot.client.ui.interface_utils import format_df_for_printout
from hummingbot.core.data_type.common import PriceType, TradeType, PositionAction, OrderType
from hummingbot.data_feed.candles_feed.data_types import CandlesConfig
from hummingbot.strategy_v2.controllers.controller_base import ControllerBase, ControllerConfigBase
from hummingbot.strategy_v2.executors.data_types import ConnectorPair
from hummingbot.strategy_v2.executors.position_executor.data_types import PositionExecutorConfig, TripleBarrierConfig
from hummingbot.strategy_v2.executors.xemm_executor.data_types import XEMMExecutorConfig
from hummingbot.strategy_v2.models.executor_actions import CreateExecutorAction, ExecutorAction, StopExecutorAction

from bots.connectors.derivative.gate_io_delivery import GateIODeliveryDerivative, GateIODeliveryAuth
from bots.connectors.derivative.bybit_delivery import BybitDeliveryDerivative, BybitDeliveryAuth

class DeliveryArbitrageConfig(ControllerConfigBase):
    controller_name: str = "delivery_arbitrage"
    candles_config: List[CandlesConfig] = []
    
    exchange1: str = Field(
        default="gateio",
        client_data=ClientFieldData(
            prompt=lambda e: "Enter the first exchange: ",
            prompt_on_new=True
        )
    )
    
    trading_pair1: str = Field(
        default="BTC-USDT",
        client_data=ClientFieldData(
            prompt=lambda e: "Enter the first trading pair: ",
            prompt_on_new=True
        )
    )
    
    exchange2: str = Field(
        default="bybit",
        client_data=ClientFieldData(
            prompt=lambda e: "Enter the second exchange: ",
            prompt_on_new=True
        )
    )
    
    trading_pair2: str = Field(
        default="BTC-USDT",
        client_data=ClientFieldData(
            prompt=lambda e: "Enter the second trading pair: ",
            prompt_on_new=True
        )
    )
    
    profitability: Decimal = Field(
        default=0.002,
        client_data=ClientFieldData(
            prompt=lambda e: "Enter the minimum profitability: ",
            prompt_on_new=True
        )
    )
    
    position_size_quote: float = Field(
        default=50,
        client_data=ClientFieldData(
            prompt=lambda e: "Enter the position size in quote currency: ",
            prompt_on_new=True
        )
    )

    def update_markets(self, markets: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
        if self.exchange1 not in markets:
            markets[self.exchange1] = set()
        markets[self.exchange1].add(self.trading_pair1)
        
        if self.exchange2 not in markets:
            markets[self.exchange2] = set()
        markets[self.exchange2].add(self.trading_pair2)
        
        return markets


class DeliveryArbitrage(ControllerBase):
    supported_exchanges = ["gateio", "bybit", "binance"]

    def __init__(self, config: DeliveryArbitrageConfig, *args, **kwargs):
        self.config = config
        super().__init__(config, *args, **kwargs)

    @property
    def exchange1_connector(self):
        return self.market_data_provider.connectors[self.config.exchange1]

    @property
    def exchange2_connector(self):
        return self.market_data_provider.connectors[self.config.exchange2]

    def create_connector(self, exchange: str, auth):
        if exchange == "gateio":
            return GateIODeliveryDerivative(auth)
        elif exchange == "bybit":
            return BybitDeliveryDerivative(auth)
        elif exchange == "binance":
            from bots.connectors.derivative.binance_futures import BinanceFuturesDerivative
            return BinanceFuturesDerivative(auth)
        raise ValueError(f"Unsupported exchange: {exchange}")

    def get_current_profitability_after_fees(self):
        """
        Calculate profitability between two delivery contracts
        """
        price1 = Decimal(self.market_data_provider.get_price_for_quote_volume(
            connector_name=self.config.exchange1,
            trading_pair=self.config.trading_pair1,
            quote_volume=self.config.position_size_quote,
            is_buy=True,
        ).result_price)
        
        price2 = Decimal(self.market_data_provider.get_price_for_quote_volume(
            connector_name=self.config.exchange2,
            trading_pair=self.config.trading_pair2,
            quote_volume=self.config.position_size_quote,
            is_buy=False,
        ).result_price)
        
        estimated_fees1 = self.exchange1_connector.get_fee(
            base_currency=self.config.trading_pair1.split("-")[0],
            quote_currency=self.config.trading_pair1.split("-")[1],
            order_type=OrderType.MARKET,
            order_side=TradeType.BUY,
            amount=self.config.position_size_quote / float(price1),
            price=price1,
            is_maker=False,
        ).percent
        
        estimated_fees2 = self.exchange2_connector.get_fee(
            base_currency=self.config.trading_pair2.split("-")[0],
            quote_currency=self.config.trading_pair2.split("-")[1],
            order_type=OrderType.MARKET,
            order_side=TradeType.BUY,
            amount=self.config.position_size_quote / float(price2),
            price=price2,
            is_maker=False,
        ).percent

        estimated_trade_pnl_pct = (price2 - price1) / price1
        return estimated_trade_pnl_pct - estimated_fees1 - estimated_fees2

    async def update_processed_data(self):
        self.processed_data = {
            "profitability": self.get_current_profitability_after_fees(),
            "price_spread": self.get_price_spread(),
            "active_arbitrage": self.is_active_arbitrage(),
            "current_pnl": self.current_pnl_pct()
        }

    def get_price_spread(self):
        """
        Get price spread between two contracts for charting
        """
        price1 = self.market_data_provider.get_price_by_type(
            self.config.exchange1,
            self.config.trading_pair1,
            PriceType.MidPrice
        )
        
        price2 = self.market_data_provider.get_price_by_type(
            self.config.exchange2,
            self.config.trading_pair2,
            PriceType.MidPrice
        )
        
        return price2 - price1
