# src/db/database.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Define the base class for the models
Base = declarative_base()

# Create the async engine
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:#@localhost/gk_books"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Session configuration
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get the session for a request
async def get_db():
    async with async_session() as session:
        yield session
