from fastapi import APIRouter, Depends
from typing import List
from src.schemas.book import BookBase, UnitBase, SubUnitBase
from src.services import BookService
from src.dependencies import get_book_service


router = APIRouter()


@router.get("/", response_model=List[BookBase])
async def get_books(book_service: BookService = Depends(get_book_service)):
    return await book_service.get_all_books()


@router.get("/book/{book_id}", response_model=BookBase)
async def get_book(book_id: int, book_service: BookService = Depends(get_book_service)):
    return await book_service.get_book_by_id(book_id)


@router.get("/book/{book_id}/units", response_model=List[UnitBase])
async def get_units(
    book_id: int, book_service: BookService = Depends(get_book_service)
):
    return await book_service.get_units_by_book_id(book_id)


@router.get("/book/unit/{unit_id}/subunits", response_model=List[SubUnitBase])
async def get_subunits(
    unit_id: int, book_service: BookService = Depends(get_book_service)
):
    return await book_service.get_subunits_by_unit_id(unit_id)
