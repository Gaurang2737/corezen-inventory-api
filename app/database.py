import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

Database_URL = os.getenv("Database_URL", "sqlite+aiosqlite:///./inventory.db")
engine = create_async_engine(Database_URL,echo= True,future = True)
AsyncSessionLocal = sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
