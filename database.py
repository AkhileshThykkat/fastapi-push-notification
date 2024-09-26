from typing import AsyncIterator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncAttrs,
    async_sessionmaker,
)


# defining engine url
sqlalchemy_url = "sqlite+aiosqlite:///database.db"

# creating an async engine
engine = create_async_engine(sqlalchemy_url, echo=False, future=True)

# creating a async session local class
SessionLocal = async_sessionmaker(
    autoflush=False, autocommit=False, bind=engine, class_=AsyncSession
)


# creating a dependency function for querying
async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

    # create a base class for creating models with asynchronous attributes


class Base(DeclarativeBase, AsyncAttrs):
    pass
