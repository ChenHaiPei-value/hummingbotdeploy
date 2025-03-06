from hummingbot.dashboard.components.config_form import ConfigForm
from .user_inputs import EXCHANGE_OPTIONS

SUPPORTED_EXCHANGES = ["gate_io", "bybit", "binance"]

def initialize(config: ConfigForm):
    config.add_select_field(
        name="exchange",
        label="选择交易所",
        options=EXCHANGE_OPTIONS,
        default="gate_io"
    )
    config.add_input_field(
        name="spread_threshold", 
        label="套利价差阈值 (%)",
        input_type="number",
        default=0.5
    )
