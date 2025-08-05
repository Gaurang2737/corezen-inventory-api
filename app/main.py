from fastapi import FastAPI
from .database import engine, Base
from .routers import products, stock

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title="CoreZen Inventory API",
    description="API for managing product inventory and stock transactions.",
    version="1.0.0",
)

@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(products.router)
app.include_router(stock.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message":"Welcome to the CoreZen Inventory Management API!"}

