from db import db
from bson import ObjectId
from schemas import Auction, Bid
from datetime import datetime

def auction_helper(auction) -> dict:
    auction["id"] = str(auction["_id"])
    auction.pop("_id")
    return auction

async def get_all_auctions():
    auctions = await db.auctions.find().to_list(100)
    return [auction_helper(a) for a in auctions]

async def get_auction_by_id(auction_id: str):
    auction = await db.auctions.find_one({"_id": ObjectId(auction_id)})
    return auction_helper(auction) if auction else None

async def create_auction(auction: Auction):
    result = await db.auctions.insert_one(auction.dict())
    return str(result.inserted_id)

async def update_auction(auction_id: str, data: dict):
    await db.auctions.update_one({"_id": ObjectId(auction_id)}, {"$set": data})

async def delete_auction(auction_id: str):
    await db.auctions.delete_one({"_id": ObjectId(auction_id)})

async def create_bid(auction_id: str, bid: Bid):
    auction = await db.auctions.find_one({"_id": ObjectId(auction_id)})
    if auction and datetime.utcnow() < auction["end_time"]:
        await db.auctions.update_one(
            {"_id": ObjectId(auction_id)},
            {"$push": {"bids": bid.dict()}}
        )
        return True
    return False

async def get_bids(auction_id: str):
    auction = await db.auctions.find_one({"_id": ObjectId(auction_id)})
    return auction["bids"] if auction else []

async def update_bid(auction_id: str, user: str, new_amount: float):
    auction = await db.auctions.find_one({"_id": ObjectId(auction_id)})
    if not auction:
        return False

    updated_bids = []
    updated = False
    for bid in auction.get("bids", []):
        if bid["user"] == user:
            bid["amount"] = new_amount
            bid["timestamp"] = datetime.utcnow()
            updated = True
        updated_bids.append(bid)

    if updated:
        await db.auctions.update_one(
            {"_id": ObjectId(auction_id)},
            {"$set": {"bids": updated_bids}}
        )
    return updated

async def get_winner(auction_id: str):
    auction = await db.auctions.find_one({"_id": ObjectId(auction_id)})
    if auction and datetime.utcnow() >= auction["end_time"]:
        if not auction["bids"]:
            return None
        winner = max(auction["bids"], key=lambda x: x["amount"])
        return winner
    return None
