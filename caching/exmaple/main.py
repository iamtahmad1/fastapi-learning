from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import SessionLocal, engine
from models import Item
import aioredis
import json
import time

app = FastAPI()
redis = None

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    global redis
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)

@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    start_time = time.perf_counter()

    cache_key = f"item:{item_id}"
    cached_item = await redis.get(cache_key)
    if cached_item:
        duration = time.perf_counter() - start_time
        return {"source": "cache", "duration_ms": round(duration * 1000, 2), "data": json.loads(cached_item)}

    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = {"id": item.id, "name": item.name}
    await redis.set(cache_key, json.dumps(item_data), ex=60)
    duration = time.perf_counter() - start_time
    return {"source": "db","duration_ms": round(duration * 1000, 2), "data": item_data}

@app.post("/items/")
async def create_item(name: str, db: AsyncSession = Depends(get_db)):
    new_item = Item(name=name)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item
