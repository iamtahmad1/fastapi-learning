from fastapi import FastAPI, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from database import AsyncSessionLocal, SessionLocal, User
import time

app = FastAPI()

# ✅ Store execution times for comparison
async_times = []
sync_times = []

# ✅ Async Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ✅ Sync Dependency
def sync_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Async API Route
@app.get("/async-users")
async def get_users(db: AsyncSession = Depends(get_db)):
    start = time.time()
    result = await db.execute(select(User))
    users = result.scalars().all()
    end = time.time()

    execution_time = end - start
    async_times.append(execution_time)  # Store time
    print(f"[ASYNC] Query Execution Time: {execution_time:.4f} seconds")

    return {"users": users, "time_taken": f"{execution_time:.4f} seconds"}

# ✅ Sync API Route
@app.get("/sync-users")
def get_users(db: Session = Depends(sync_get_db)):
    start = time.time()
    users = db.query(User).all()
    end = time.time()

    execution_time = end - start
    sync_times.append(execution_time)  # Store time
    print(f"[SYNC] Query Execution Time: {execution_time:.4f} seconds")

    return {"users": users, "time_taken": f"{execution_time:.4f} seconds"}

# ✅ Compare Sync vs Async Route
@app.get("/compare")
def compare():
    async_avg = sum(async_times) / len(async_times) if async_times else 0
    sync_avg = sum(sync_times) / len(sync_times) if sync_times else 0

    print("\n--- Performance Comparison ---")
    print(f"🔵 Average ASYNC Query Time: {async_avg:.4f} seconds")
    print(f"🔴 Average SYNC Query Time: {sync_avg:.4f} seconds")
    print("------------------------------\n")

    return {
        "async_avg_time": f"{async_avg:.4f} seconds",
        "sync_avg_time": f"{sync_avg:.4f} seconds",
    }
