# Delivery Contract Arbitrage Strategy

This strategy implements an arbitrage strategy between delivery contracts, either within the same exchange or across different exchanges.

## Key Features

- Cross-contract arbitrage
- Configurable profit thresholds
- Position size management
- Slippage protection
- Funding rate monitoring
- Multi-exchange support

## Configuration Parameters

### Contract 1
- `contract1_connector`: Exchange connector for first contract (default: gate_io)
- `contract1_trading_pair`: Trading pair for first contract (e.g. BTC-USD)
- `contract1_leverage`: Leverage for first contract (default: 1.0)
- `contract1_delivery_date`: Delivery date for first contract

### Contract 2
- `contract2_connector`: Exchange connector for second contract (default: gate_io)
- `contract2_trading_pair`: Trading pair for second contract (e.g. BTC-USD)
- `contract2_leverage`: Leverage for second contract (default: 1.0)
- `contract2_delivery_date`: Delivery date for second contract

### Arbitrage Parameters
- `min_profitability`: Minimum profitability threshold (default: 0.2%)
- `max_profitability`: Maximum profitability threshold (default: 1.0%)
- `max_position_size`: Maximum position size in USD (default: 1000)
- `hedge_ratio`: Hedge ratio between contracts (default: 1.0)
- `slippage_tolerance`: Maximum allowed slippage (default: 0.1%)
- `funding_rate_threshold`: Funding rate threshold to avoid (default: 0.01%)

## How It Works

1. Monitors price differences between delivery contracts
2. Executes trades when profitability exceeds configured thresholds
3. Manages position sizes and hedges according to configured parameters
4. Monitors funding rates and adjusts positions accordingly
5. Automatically closes positions before delivery dates

## Supported Scenarios

- Same exchange, different delivery dates
- Different exchanges, same delivery date
- Different exchanges, different delivery dates

## Risk Management

- Position size limits
- Slippage protection
- Funding rate monitoring
- Automatic position closing before delivery
- Exchange connectivity monitoring
