from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException
from typing import List, Dict, Optional
from src.models.question import Question
from src.models.choice import Choice


class QuizService:
    def __init__(self, db: AsyncSession):
        # Initializes the QuizService with the given database session
        self.db = db

    # Helper method to fetch questions with their associated choices, unit, subunit, and book
    async def _get_questions_with_choices(
        self, question_filter
    ) -> List[Dict[str, any]]:
        """
        Fetches all questions and their related choices, book, unit, and subunit based on a filter.
        Uses `selectinload` to efficiently load choices, unit, subunit, and book along with questions.
        """
        async with self.db.begin():
            result = await self.db.execute(
                select(Question)
                .filter(question_filter)
                .options(
                    selectinload(Question.choices),  # Efficiently load choices
                    selectinload(Question.subunit),  # Efficiently load subunit
                    selectinload(
                        Question.subunit.unit
                    ),  # Efficiently load unit via subunit
                    selectinload(
                        Question.subunit.unit.book
                    ),  # Efficiently load book via unit
                )
            )
            questions = result.scalars().all()

        if not questions:
            raise HTTPException(status_code=404, detail="No questions found")

        # Formats questions and choices to be returned in the response
        return [
            {
                "id": question.id,
                "text_en": question.text_en,
                "text_hi": question.text_hi,
                "book": {
                    "id": question.subunit.unit.book.id,
                    "title_en": question.subunit.unit.book.title_en,
                    "title_hi": question.subunit.unit.book.title_hi,
                },
                "unit": {
                    "id": question.subunit.unit.id,
                    "title_en": question.subunit.unit.title_en,
                    "title_hi": question.subunit.unit.title_hi,
                },
                "subunit": {
                    "id": question.subunit.id,
                    "title_en": question.subunit.title_en,
                    "title_hi": question.subunit.title_hi,
                },
                "choices": [
                    {
                        "id": choice.id,
                        "text_en": choice.text_en,
                        "text_hi": choice.text_hi,
                    }
                    for choice in question.choices
                ],
            }
            for question in questions
        ]

    # Method to get question with choices by question_id
    async def get_question_with_choices(self, question_id: int) -> Dict[str, any]:
        """
        Fetches a single question by its ID, along with its associated choices, book, unit, and subunit.
        Returns the question and choices in the expected format.
        """
        questions = await self._get_questions_with_choices(Question.id == question_id)

        if not questions:
            raise HTTPException(status_code=404, detail="Question not found")

        return questions[0]  # Return the first (and only) question

    # Method to handle the submission of an answer
    async def submit_answer(self, question_id: int, choice_id: int) -> Dict[str, any]:
        """
        Handles the answer submission by checking if the selected choice is correct.
        Returns a message indicating whether the answer is correct or incorrect.
        """
        questions = await self._get_questions_with_choices(Question.id == question_id)

        if not questions:
            raise HTTPException(status_code=404, detail="Question not found")

        # Find the selected choice within the pre-loaded choices
        question = questions[0]
        choice = next((ch for ch in question["choices"] if ch["id"] == choice_id), None)

        if not choice:
            raise HTTPException(status_code=404, detail="Choice not found")

        # Check if the submitted choice is correct
        if choice["is_correct"]:
            return {"message": "Correct answer!", "correct": True}
        else:
            return {"message": "Incorrect answer. Try again!", "correct": False}

    # Method to get questions by subunit_id with choices (without correct answer flag)
    async def get_questions_by_subunit(self, subunit_id: int) -> List[Dict[str, any]]:
        """
        Fetches all questions related to a specific subunit, including their choices.
        The correct answer flag is not included in the choices.
        """
        return await self._get_questions_with_choices(Question.subunit_id == subunit_id)
