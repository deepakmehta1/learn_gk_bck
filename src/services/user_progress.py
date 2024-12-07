from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.models import UserProgress, User
from src.enums.enums import QuestionStatus
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker


class UserProgressService:
    def __init__(self, db: AsyncSession, user: User = None):
        """
        Initialize the service with a user and the database session.
        """
        self.db = db
        self.user = user

    def associate_user(self, user: User) -> None:
        self.user = user

    async def update_user_progress(
        self,
        book_id: int,
        unit_id: int,
        sub_unit_id: int,
        question_id: int,
        selected_choice: int,
        is_correct: bool,
        status: QuestionStatus = QuestionStatus.READ,
    ):
        """
        Updates or creates a user progress record for a given question.

        If the user has not previously attempted the question, it creates a new progress record.
        If the user has previously attempted the question, it updates their selected choice and status.
        """
        # Check if a progress entry exists for the user and the specific question
        async with self.db.begin():
            result = await self.db.execute(
                select(UserProgress).filter(
                    UserProgress.user_id == self.user.id,
                    UserProgress.book_id == book_id,
                    UserProgress.unit_id == unit_id,
                    UserProgress.sub_unit_id == sub_unit_id,
                    UserProgress.question_id == question_id,
                )
            )
            progress = result.scalars().first()

        if progress:
            # If progress exists, update the selected_choice and is_correct
            progress.selected_choice = selected_choice
            progress.is_correct = is_correct
            progress.status = status  # Update the status (e.g., "read", "submitted")
        else:
            # If no progress exists, create a new record for the user's progress
            progress = UserProgress(
                user_id=self.user.id,
                book_id=book_id,
                unit_id=unit_id,
                sub_unit_id=sub_unit_id,
                question_id=question_id,
                selected_choice=selected_choice,
                is_correct=is_correct,
                status=status,
            )
            self.db.add(progress)

        # Commit the changes (insert or update)
        await self.db.commit()
        await self.db.refresh(progress)
        return progress
