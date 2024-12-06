from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.models import User
from src.services import QuizService, UserService, BookService, UserProgressService

from firebase_admin import auth
from src.firebase import firebase_admin

from typing import Optional


def get_book_service(db: AsyncSession = Depends(get_db)) -> BookService:
    return BookService(db)


def get_quiz_service(db: AsyncSession = Depends(get_db)) -> QuizService:
    return QuizService(db)


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_user_progress_service(
    db: AsyncSession = Depends(get_db),
) -> UserProgressService:
    return UserProgressService(db)


def get_user_email_from_token(authorization: Optional[str] = Header(None)) -> str:
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
