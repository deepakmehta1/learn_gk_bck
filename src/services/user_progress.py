from typing import Dict
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import UserProgress, User, SubUnit, Unit, Book
from src.enums.enums import QuestionStatus
from sqlalchemy.future import select
from src.services import QuizService


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

    async def get_user_progress_by_type(
        self, quiz_service: QuizService, progress_type: str, type_id: int
    ) -> Dict[str, any]:
        """
        Fetch user progress based on the specified type and type_id.
        Type can be 'book', 'unit', or 'subunit'.
        """
        if progress_type == "book":
            # Fetch user progress for the specified book
            result = await self.db.execute(
                select(UserProgress)
                .filter(UserProgress.book_id == type_id)
                .order_by(UserProgress.updated_at.desc())
            )
            user_progress = result.scalars().all()

            book = await self.db.execute(select(Book).filter(Book.id == type_id))
            book = book.scalars().first()
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")

            total_questions = await quiz_service.get_total_questions_by_book(book)

        elif progress_type == "unit":
            # Fetch user progress for the specified unit
            result = await self.db.execute(
                select(UserProgress)
                .filter(UserProgress.unit_id == type_id)
                .order_by(UserProgress.updated_at.desc())
            )
            user_progress = result.scalars().all()

            unit = await self.db.execute(select(Unit).filter(Unit.id == type_id))
            unit = unit.scalars().first()
            if not unit:
                raise HTTPException(status_code=404, detail="Unit not found")

            total_questions = await quiz_service.get_questions_by_unit(unit)

        elif progress_type == "subunit":
            # Fetch user progress for the specified subunit
            result = await self.db.execute(
                select(UserProgress)
                .filter(UserProgress.sub_unit_id == type_id)
                .order_by(UserProgress.updated_at.desc())
            )
            user_progress = result.scalars().all()

            subunit = await self.db.execute(
                select(SubUnit).filter(SubUnit.id == type_id)
            )
            subunit = subunit.scalars().first()
            if not subunit:
                raise HTTPException(status_code=404, detail="Subunit not found")

            total_questions = await quiz_service.get_questions_by_subunit(subunit)

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid progress type. Must be one of: book, unit, subunit.",
            )

        # Calculate total questions attempted and correct
        total_attempted = sum(1 for up in user_progress if up.status == "submitted")
        total_correct = sum(1 for up in user_progress if up.is_correct)

        # Calculate accuracy as a percentage
        accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0

        # Fetch the most recent question details
        recent_question_details = [
            {
                "unit_id": up.unit_id,
                "sub_unit_id": up.sub_unit_id,
                "question_id": up.question_id,
                "status": up.status,
            }
            for up in user_progress
        ]

        # Build the response as a dictionary
        response = {
            "total_questions": len(total_questions),
            "total_questions_attempted": total_attempted,
            "total_questions_correct": total_correct,
            "accuracy": round(accuracy, 2),
            "recent_question_details": recent_question_details[:1],
        }

        return response
