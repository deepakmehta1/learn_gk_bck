from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.book import Book

async def get_book_by_id(db: AsyncSession, book_id: int):
    async with db.begin():
        result = await db.execute(select(Book).filter(Book.id == book_id))
        return result.scalars().first()
