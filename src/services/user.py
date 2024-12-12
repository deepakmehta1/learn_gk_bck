from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from src.models.user import (
    User,
)  # Assuming the User model is defined in src/models/user.py


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User:
        """
        Fetch a user by email from the database.

        Parameters:
        - email: str - The email of the user to retrieve.

        Returns:
        - User: The user object with the specified email.

        Raises:
        - HTTPException: If no user with the provided email exists.
        """
        # Query to fetch the user by email
        result = await self.db.execute(select(User).filter(User.email == email))
        user = (
            result.scalars().first()
        )  # Get the first result (there should only be one)

        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with email {email} not found"
            )

        return user
