from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.services import QuizService, UserService
from firebase_admin import auth
from src.firebase import firebase_admin
from typing import Optional


def get_quiz_service(db: AsyncSession = Depends(get_db)) -> QuizService:
    return QuizService(db)


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


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
