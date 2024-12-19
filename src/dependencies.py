from fastapi import Depends, HTTPException, Header
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.models import User, SubUnit, Question
from src.enums import SubscriptionTypeEnum
from src.services import (
    QuizService,
    UserService,
    BookService,
    UserProgressService,
    SubscriptionService,
)

from firebase_admin import auth
from src.firebase import firebase_admin
from typing import Optional


async def get_subscription_service(db: AsyncSession = Depends(get_db)) -> BookService:
    return SubscriptionService(db)


async def get_book_service(db: AsyncSession = Depends(get_db)) -> BookService:
    return BookService(db)


async def get_quiz_service(db: AsyncSession = Depends(get_db)) -> QuizService:
    return QuizService(db)


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


async def get_user_progress_service(
    db: AsyncSession = Depends(get_db),
) -> UserProgressService:
    return UserProgressService(db)


async def get_user_email_from_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Dependency function to extract the Bearer token from the header, verify it via Firebase,
    and return the respective user's email.
    """
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # Check if the token starts with 'Bearer ' and extract the token
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else None

    if token is None:
        raise HTTPException(status_code=401, detail="Bearer token missing or malformed")

    try:
        # Verify the Firebase token
        decoded_token = auth.verify_id_token(token)
        # Extract the email from the decoded token
        user_email = decoded_token.get("email")
        if not user_email:
            raise HTTPException(status_code=401, detail="Email not found in the token")
        return user_email

    except Exception as e:
        # If verification fails, raise an HTTPException
        raise HTTPException(status_code=401, detail="Invalid token or token expired")


async def get_current_user(
    user_email: str = Depends(get_user_email_from_token),
    user_service: UserService = Depends(get_user_service),
) -> User:
    user = await user_service.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def check_user_subscription_and_preview(
    question_id: int = None,
    subunit_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
) -> bool:
    """
    Check if the current user has a subscription (full or specific book) and if the subunit is previewed.
    """

    # If subunit_id is provided, directly use it
    if subunit_id:
        # Await the execution of the query
        subunit_result = await db.execute(
            select(SubUnit).filter(SubUnit.id == subunit_id)
        )
        subunit = subunit_result.scalars().first()

    # If question_id is provided, fetch the subunit_id from the Question table
    elif question_id:
        # Await the execution of the query
        question_result = await db.execute(
            select(Question).filter(Question.id == question_id)
        )
        question = question_result.scalars().first()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        subunit = (
            question.subunit
        )  # Get subunit directly from the related `subunit` field

    else:
        raise HTTPException(
            status_code=400, detail="Either subunit_id or question_id must be provided"
        )

    if not subunit:
        raise HTTPException(status_code=404, detail="Subunit not found")

    # If the subunit is previewed, allow access without subscription
    if subunit.preview:
        return True  # Subunit is previewed, no need for subscription check

    # Check if the user has full subscription
    subscription = await subscription_service.check_user_has_a_full_subscription(
        user_id=current_user.id
    )
    if subscription:
        return True

    # Check if the user has a subscription
    subscription = await subscription_service.check_user_subscription_for_book(
        user_id=current_user.id, book_id=subunit.unit.book_id
    )

    return True if subscription else False
