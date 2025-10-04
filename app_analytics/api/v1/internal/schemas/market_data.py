from pydantic import BaseModel, Field


class MarketDataSchema(BaseModel):
        ticket: str = Field(..., description="Ticker symbol"),
        date: str = Field(..., description="Date and time in ISO 8601 format")
        open: float = Field(..., description="Opening price")
        high: float = Field(..., description="Highest price")
        low : float = Field(..., description="Lowest price")
        close : float = Field(..., description="Closing price")
        volume: int = Field(..., description="Trading volume")

class PostMarketDataRequestSchema(BaseModel):
    data: list[MarketDataSchema] = Field(..., description="List of market data entries")
