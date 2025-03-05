import plotly.graph_objects as go
import streamlit as st
import yaml
from datetime import datetime

from frontend.st_utils import get_backend_api_client, initialize_st_page

# Initialize the Streamlit page
initialize_st_page(title="Gate.io Delivery Contract Arbitrage", icon="⚡️")

# Page content
st.text("This tool will let you create a config for Gate.io Delivery Contract Arbitrage and upload it to the BackendAPI.")
st.write("---")

# Strategy parameters
c1, c2 = st.columns([1, 1])
with c1:
    spot_connector = st.text_input("Spot Connector", value="gate_io")
    spot_trading_pair = st.text_input("Spot Trading Pair", value="BTC-USDT")
    spot_leverage = st.number_input("Spot Leverage", value=1.0, step=0.1)
    
with c2:
    delivery_connector = st.text_input("Delivery Connector", value="gate_io")
    delivery_trading_pair = st.text_input("Delivery Trading Pair", value="BTC-USD")
    delivery_leverage = st.number_input("Delivery Leverage", value=1.0, step=0.1)
    delivery_date = st.date_input("Delivery Date", value=datetime.now())

# Arbitrage parameters
st.write("---")
c3, c4 = st.columns([1, 1])
with c3:
    min_profitability = st.number_input("Min Profitability (%)", value=0.2, step=0.01) / 100
    max_profitability = st.number_input("Max Profitability (%)", value=1.0, step=0.01) / 100
    max_position_size = st.number_input("Max Position Size (USD)", value=1000, step=100)

with c4:
    hedge_ratio = st.number_input("Hedge Ratio", value=1.0, step=0.1)
    slippage_tolerance = st.number_input("Slippage Tolerance (%)", value=0.1, step=0.01) / 100
    funding_rate_threshold = st.number_input("Funding Rate Threshold (%)", value=0.01, step=0.001) / 100

# Config upload
st.write("---")
c5, c6 = st.columns([2, 1])
with c5:
    config_base = st.text_input("Config Base", 
                              value=f"gate-delivery-arb-{spot_trading_pair.split('-')[0]}")
with c6:
    config_tag = st.text_input("Config Tag", value="1.0")

id = f"{config_base}_{config_tag}"
config = {
    "id": id.lower(),
    "controller_name": "gate_delivery_arb",
    "controller_type": "arbitrage",
    "spot_connector": spot_connector,
    "spot_trading_pair": spot_trading_pair,
    "spot_leverage": spot_leverage,
    "delivery_connector": delivery_connector,
    "delivery_trading_pair": delivery_trading_pair,
    "delivery_leverage": delivery_leverage,
    "delivery_date": delivery_date.strftime("%Y-%m-%d"),
    "min_profitability": min_profitability,
    "max_profitability": max_profitability,
    "max_position_size": max_position_size,
    "hedge_ratio": hedge_ratio,
    "slippage_tolerance": slippage_tolerance,
    "funding_rate_threshold": funding_rate_threshold
}

yaml_config = yaml.dump(config, default_flow_style=False)

with c6:
    upload_config_to_backend = st.button("Upload Config to BackendAPI")

if upload_config_to_backend:
    backend_api_client = get_backend_api_client()
    backend_api_client.add_controller_config(config)
    st.success("Config uploaded successfully!")
