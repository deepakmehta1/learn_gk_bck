from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException
from src.models import Book, Unit, SubUnit, Question
from src.schemas.book import BookBase, UnitBase, SubUnitBase
from typing import List, Dict


class BookService:
    def __init__(self, db: AsyncSession):
        # Initializes the BookService with the given database session
        self.db = db

    async def get_all_books(self) -> List[BookBase]:
        """
        Fetches all books along with their units and subunits.
        Uses `get_book_by_id` to get full details for each book.
        """
        # Fetch all books
        async with self.db.begin():
            result = await self.db.execute(
                select(Book)
            )  # Fetch books without joining units/subunits
            books = result.scalars().all()

        if not books:
            raise HTTPException(status_code=404, detail="No books found")

        # Fetch detailed information (units, subunits, and question counts) for each book
        books_with_details = []
        for book in books:
            book_details = await self.get_book_by_id(book.id)
            books_with_details.append(book_details)

        return books_with_details

    async def get_book_by_id(self, book_id: int) -> Dict[str, any]:
        """
        Fetches a single book by its ID along with its units and subunits.
        Uses the existing methods to get question counts for each unit and subunit.
        """
        # Fetch the book with its units
        async with self.db.begin():
            result = await self.db.execute(select(Book).filter(Book.id == book_id))
            book = result.scalars().first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # Fetch the units for the book
        units = await self.get_units_by_book_id(book_id)

        # For each unit, fetch subunits and question count per subunit
        for unit in units:
            unit_id = unit["id"]
            # Get subunits with their question count
            subunits = await self.get_subunits_by_unit_id(unit_id)
            unit["subunits"] = subunits

        # Combine the book data with its units and subunits
        return {
            "id": book.id,
            "title_en": book.title_en,
            "title_hi": book.title_hi,
            "units": units,
        }

    async def get_units_by_book_id(self, book_id: int) -> List[UnitBase]:
        """
        Fetches all units for a specific book, along with their subunits and question counts.
        """
        async with self.db.begin():
            result = await self.db.execute(select(Unit).filter(Unit.book_id == book_id))
            units = result.scalars().all()

        if not units:
            raise HTTPException(status_code=404, detail="No units found for this book")

        # Add question count to each unit
        for unit in units:
            unit.question_count = len(unit.subunits)

        return [
            {
                "id": unit.id,
                "title_en": unit.title_en,
                "title_hi": unit.title_hi,
                "question_count": unit.question_count,
            }
            for unit in units
        ]

    async def get_subunits_by_unit_id(self, unit_id: int) -> List[SubUnitBase]:
        """
        Fetches all subunits for a specific unit, including the count of questions per subunit.
        """
        async with self.db.begin():
            result = await self.db.execute(
                select(SubUnit)
                .filter(SubUnit.unit_id == unit_id)
                .join(Question, Question.subunit_id == SubUnit.id, isouter=True)
                .group_by(SubUnit.id)
                .add_columns(func.count(Question.id).label("question_count"))
            )
            subunits = result.all()

        if not subunits:
            raise HTTPException(
                status_code=404, detail="No subunits found for this unit"
            )

        return [
            {
                "id": subunit.id,
                "title_en": subunit.title_en,
                "title_hi": subunit.title_hi,
                "question_count": question_count,
            }
            for subunit, question_count in subunits
        ]
