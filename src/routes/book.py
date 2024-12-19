from fastapi import APIRouter, Depends
from typing import List
from pydantic import TypeAdapter
from src.schemas.book import BookBase, UnitBase, SubUnitBase
from src.services import BookService, SubscriptionService, UserService
from src.dependencies import (
    get_book_service,
    get_current_user,
    get_subscription_service,
)


router = APIRouter()


@router.get("/", response_model=List[BookBase])
async def get_books(
    book_service: BookService = Depends(get_book_service),
    current_service: UserService = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    books = await book_service.get_all_books()
    books = TypeAdapter(List[BookBase]).validate_python(books)
    for book in books:
        full_subscription = (
            await subscription_service.check_user_has_a_full_subscription(
                current_service.id
            )
        )

        if full_subscription:
            for unit in book.units:
                for subunit in unit.subunits:
                    subunit.is_preview = True
        else:
            book_subscription = (
                await subscription_service.check_user_subscription_for_book(
                    current_service.id, book.id
                )
            )
            if book_subscription:
                for unit in book.units:
                    for subunit in unit.subunits:
                        subunit.is_preview = True

    return books


@router.get("/book/{book_id}", response_model=BookBase)
async def get_book(
    book_id: int,
    book_service: BookService = Depends(get_book_service),
    current_service: UserService = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    book = await book_service.get_book_by_id(book_id)
    book = BookBase.model_validate(book)
    full_subscription = await subscription_service.check_user_has_a_full_subscription(
        current_service.id
    )
    if full_subscription:
        for unit in book.units:
            for subunit in unit.subunits:
                subunit.is_preview = True
    else:
        book_subscription = await subscription_service.check_user_subscription_for_book(
            current_service.id, book_id
        )
        if book_subscription:
            for unit in book.units:
                for subunit in unit.subunits:
                    subunit.is_preview = True
    return book


@router.get("/book/{book_id}/units", response_model=List[UnitBase])
async def get_units(
    book_id: int,
    book_service: BookService = Depends(get_book_service),
    current_service: UserService = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    units = await book_service.get_units_by_book_id(book_id)
    units = TypeAdapter(List[UnitBase]).validate_python(units)
    full_subscription = await subscription_service.check_user_has_a_full_subscription(
        current_service.id
    )
    if full_subscription:
        for unit in units:
            for subunit in unit.subunits:
                subunit.is_preview = True
    else:
        book_subscription = await subscription_service.check_user_subscription_for_book(
            current_service.id, book_id
        )
        if book_subscription:
            for unit in units:
                for subunit in unit.subunits:
                    subunit.is_preview = True
    return units


@router.get("/book/unit/{unit_id}/subunits", response_model=List[SubUnitBase])
async def get_subunits(
    unit_id: int,
    book_service: BookService = Depends(get_book_service),
    current_service: UserService = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    subunits = await book_service.get_subunits_by_unit_id(unit_id)
    book = await book_service.get_book_by_unit_id(unit_id)
    subunits = TypeAdapter(List[SubUnitBase]).validate_python(subunits)
    full_subscription = await subscription_service.check_user_has_a_full_subscription(
        current_service.id
    )
    if full_subscription:
        for subunit in subunits:
            subunit.is_preview = True
    else:
        book_subscription = await subscription_service.check_user_subscription_for_book(
            current_service.id, book.id
        )
        if book_subscription:
            for subunit in subunits:
                subunit.is_preview = True
    return subunits
