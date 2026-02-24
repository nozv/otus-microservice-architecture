from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from src.config import get_db_url
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_local = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase): pass

async def get_session() -> AsyncSession:
    async with async_session_local() as session:
        yield session