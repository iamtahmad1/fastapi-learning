from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine, Column, Integer, String

DATABASE_URL_ASYNC = "postgresql+asyncpg://testuser:testpass@10.114.104.157/testdb"
DATABASE_URL_SYNC = "postgresql://testuser:testpass@10.114.104.157/testdb"

# ✅ Async Engine & Session
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# ✅ Sync Engine & Session
sync_engine = create_engine(DATABASE_URL_SYNC, echo=True)
SessionLocal = sessionmaker(bind=sync_engine, class_=Session)

Base = declarative_base()

# ✅ User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)

# ✅ Async function to create tables
async def init_db_async():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ✅ Sync function to create tables
def init_db_sync():
    Base.metadata.create_all(bind=sync_engine)
