from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Connection URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:#@localhost/gk_books"

# Create the asynchronous engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Session configuration
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for our models
Base = declarative_base()

# Dependency to get the session for a request
async def get_db():
    async with async_session() as session:
        yield session
