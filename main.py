from fastapi import FastAPI
from routes.auctions import router as auction_router
from db import client

app = FastAPI()

@app.on_event("startup")
async def connect_to_mongo():
    try:
        await client.admin.command("ping")
        print("✅ Conexión exitosa a MongoDB Atlas")
    except Exception as e:
        print("❌ Error al conectar con MongoDB:", e)

app.include_router(auction_router)

@app.get("/")
def root():
    return {"message": "Auction API is running"}
