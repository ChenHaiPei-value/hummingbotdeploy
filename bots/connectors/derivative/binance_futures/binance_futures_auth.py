from pydantic import BaseModel, Field
from hummingbot.client.config.config_data_types import ClientFieldData

class BinanceFuturesAuth(BaseModel):
    api_key: str = Field(
        default="",
        client_data=ClientFieldData(
            prompt=lambda e: "Enter your Binance Futures API key",
            is_secure=True,
            prompt_on_new=True
        )
    )
    
    api_secret: str = Field(
        default="",
        client_data=ClientFieldData(
            prompt=lambda e: "Enter your Binance Futures API secret",
            is_secure=True,
            prompt_on_new=True
        )
    )
