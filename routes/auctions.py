from fastapi import APIRouter, HTTPException
from schemas import Auction, Bid, UpdateBid, CreateBid
from models import (
    get_all_auctions, get_auction_by_id, create_auction,
    update_auction, delete_auction, create_bid,
    get_bids, update_bid, get_winner
)

router = APIRouter(prefix="/auctions")

@router.get("/")
async def list_auctions():
    return await get_all_auctions()

@router.get("/{auction_id}")
async def auction_detail(auction_id: str):
    auction = await get_auction_by_id(auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    return auction

@router.post("/")
async def create_new_auction(auction: Auction):
    auction_id = await create_auction(auction)
    return {"message": "Auction created", "id": auction_id}

@router.put("/{auction_id}")
async def update_auction_details(auction_id: str, data: dict):
    await update_auction(auction_id, data)
    return {"message": "Auction updated"}

@router.delete("/{auction_id}")
async def remove_auction(auction_id: str):
    await delete_auction(auction_id)
    return {"message": "Auction deleted"}

@router.post("/{auction_id}/bids")
async def bid_on_auction(auction_id: str, bid: CreateBid):
    full_bid = Bid(**bid.dict())  
    success = await create_bid(auction_id, full_bid)
    if not success:
        raise HTTPException(status_code=400, detail="Bid rejected")
    return {"message": "Bid accepted"}

@router.get("/{auction_id}/bids")
async def list_bids(auction_id: str):
    return await get_bids(auction_id)

@router.put("/{auction_id}/bids/{user}")
async def modify_bid(auction_id: str, user: str, data: UpdateBid):
    updated = await update_bid(auction_id, user, data.amount)
    if not updated:
        raise HTTPException(status_code=404, detail="Bid not found")
    return {"message": "Bid updated"}

@router.get("/{auction_id}/winner")
async def get_auction_winner(auction_id: str):
    result = await get_winner(auction_id)
    if result is None:
        return {"message": "No hay pujas registradas en esta subasta."}
    return result

