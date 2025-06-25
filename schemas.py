from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Bid(BaseModel):
    user: str
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CreateBid(BaseModel):
    user: str
    amount: float

class UpdateBid(BaseModel):
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Auction(BaseModel):
    title: str
    description: Optional[str] = None
    end_time: datetime
    bids: List[Bid] = []

class AuctionInDB(Auction):
    id: Optional[str] = None