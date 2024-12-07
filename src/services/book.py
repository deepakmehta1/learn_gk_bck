from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from src.models import Book, Unit, SubUnit
from src.schemas.book import BookBase, UnitBase, SubUnitBase
from typing import List


class BookService:
    def __init__(self, db: AsyncSession):
        # Initializes the BookService with the given database session
        self.db = db

    async def get_all_books(self) -> List[BookBase]:
        """
        Fetches all books along with their units and subunits.
        """
        async with self.db.begin():
            result = await self.db.execute(select(Book))  # No selectinload here
            books = result.scalars().all()

        if not books:
            raise HTTPException(status_code=404, detail="No books found")

        return books

    async def get_book_by_id(self, book_id: int) -> BookBase:
        """
        Fetches a single book by its ID along with its units and subunits.
        """
        async with self.db.begin():
            result = await self.db.execute(
                select(Book).filter(Book.id == book_id)
            )  # No selectinload here
            book = result.scalars().first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        return book

    async def get_units_by_book_id(self, book_id: int) -> List[UnitBase]:
        """
        Fetches all units for a specific book.
        """
        async with self.db.begin():
            result = await self.db.execute(
                select(Unit).filter(Unit.book_id == book_id)
            )  # No selectinload here
            units = result.scalars().all()

        if not units:
            raise HTTPException(status_code=404, detail="No units found for this book")

        return units

    async def get_subunits_by_unit_id(self, unit_id: int) -> List[SubUnitBase]:
        """
        Fetches all subunits for a specific unit.
        """
        async with self.db.begin():
            result = await self.db.execute(
                select(SubUnit).filter(SubUnit.unit_id == unit_id)
            )  # No selectinload here
            subunits = result.scalars().all()

        if not subunits:
            raise HTTPException(
                status_code=404, detail="No subunits found for this unit"
            )

        return subunits
