import streamlit as st

def get_user_inputs():
    """Get user inputs for delivery contract arbitrage strategy"""
    inputs = {}
    
    # Contract 1 parameters
    c1, c2 = st.columns([1, 1])
    with c1:
        inputs['contract1_connector'] = st.text_input("Contract 1 Connector", value="gate_io")
        inputs['contract1_trading_pair'] = st.text_input("Contract 1 Trading Pair", value="BTC-USD")
        inputs['contract1_leverage'] = st.number_input("Contract 1 Leverage", value=1.0, step=0.1)
        inputs['contract1_delivery_date'] = st.date_input("Contract 1 Delivery Date")
        
    # Contract 2 parameters
    with c2:
        inputs['contract2_connector'] = st.text_input("Contract 2 Connector", value="gate_io")
        inputs['contract2_trading_pair'] = st.text_input("Contract 2 Trading Pair", value="BTC-USD")
        inputs['contract2_leverage'] = st.number_input("Contract 2 Leverage", value=1.0, step=0.1)
        inputs['contract2_delivery_date'] = st.date_input("Contract 2 Delivery Date")

    # Arbitrage parameters
    st.write("---")
    c3, c4 = st.columns([1, 1])
    with c3:
        inputs['min_profitability'] = st.number_input("Min Profitability (%)", value=0.2, step=0.01) / 100
        inputs['max_profitability'] = st.number_input("Max Profitability (%)", value=1.0, step=0.01) / 100
        inputs['max_position_size'] = st.number_input("Max Position Size (USD)", value=1000, step=100)

    with c4:
        inputs['hedge_ratio'] = st.number_input("Hedge Ratio", value=1.0, step=0.1)
        inputs['slippage_tolerance'] = st.number_input("Slippage Tolerance (%)", value=0.1, step=0.01) / 100
        inputs['funding_rate_threshold'] = st.number_input("Funding Rate Threshold (%)", value=0.01, step=0.001) / 100

    return inputs
