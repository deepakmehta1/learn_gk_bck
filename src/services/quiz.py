from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException
from typing import List, Dict
from src.models import Question, Book, Unit, SubUnit


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
        The relationships are preloaded via `lazy="selectin"` in the models.
        """
        result = await self.db.execute(select(Question).filter(question_filter))
        questions = result.scalars().all()

        if not questions:
            raise HTTPException(status_code=404, detail="No questions found")

        return questions

    # Method to get question with choices by question_id
    async def get_question_with_choices(self, question_id: int) -> Dict[str, any]:
        """
        Fetches a single question by its ID, along with its associated choices, book, unit, and subunit.
        Returns the question and choices in the expected format.
        """
        questions = await self._get_questions_with_choices(Question.id == question_id)

        if not questions:
            raise HTTPException(status_code=404, detail="Question not found")

        question = questions[0]
        return {
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

    # Method to handle the submission of an answer
   # Method to handle the submission of an answer
    async def submit_answer(self, question_id: int, choice_id: int) -> Dict[str, any]:
        """
        Handles the answer submission by checking if the selected choice is correct.
        Returns a message indicating whether the answer is correct or incorrect,
        and also includes the correct option id.
        """
        # Fetch the question with choices
        questions = await self._get_questions_with_choices(Question.id == question_id)

        if not questions:
            raise HTTPException(status_code=404, detail="Question not found")

        # Get the question and choices
        question = questions[0]
        
        # Find the selected choice
        choice = next((ch for ch in question.choices if ch.id == choice_id), None)

        if not choice:
            raise HTTPException(status_code=404, detail="Choice not found")

        # Find the correct choice for this question
        correct_choice = next((ch for ch in question.choices if ch.is_correct), None)

        if not correct_choice:
            raise HTTPException(status_code=500, detail="No correct answer found for the question")

        # Check if the selected choice is correct
        is_correct = choice.id == correct_choice.id

        # Return the result with the correct option id
        return {
            "message": "Correct answer!" if is_correct else "Incorrect answer. Try again!",
            "correct": is_correct,
            "correct_option_id": correct_choice.id  # Add the correct option id to the response
        }


    # Method to get questions by subunit_id with choices (without correct answer flag)
    async def get_questions_by_subunit_id(self, subunit_id: int) -> List[Dict[str, any]]:
        """
        Fetches all questions related to a specific subunit, including their choices.
        The correct answer flag is not included in the choices.
        """
        questions = await self._get_questions_with_choices(
            Question.subunit_id == subunit_id
        )

        return [
            {
                "id": question.id,
                "text_en": question.text_en,
                "text_hi": question.text_hi,
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

    async def get_total_questions_by_book(self, book: Book) -> List[Question]:
        """
        Returns all the questions across all units and subunits for this book.
        """
        query = await self.db.execute(
            select(Question)  # Select Question instances
            .join(Unit, Unit.book_id == book.id)  # Join with Unit
            .join(SubUnit, SubUnit.unit_id == Unit.id)  # Join with SubUnit
            .filter(Question.subunit_id == SubUnit.id)  # Join with Question on Subunit
        )

        # Extract the list of questions
        questions = query.scalars().all()

        if not questions:
            return []  # Return an empty list if no questions found

        return questions

    async def get_questions_by_unit(self, unit: Unit) -> List[Question]:
        """
        Fetches all questions associated with a specific unit.
        """
        # Query to get questions for the specific unit
        query = await self.db.execute(
            select(Question)
            .join(SubUnit, SubUnit.id == Question.subunit_id)
            .filter(SubUnit.unit_id == unit.id)  # Filter by unit
        )

        questions = query.scalars().all()  # Fetch all the questions

        if not questions:
            return []  # Return an empty list if no questions found

        return questions

    async def get_questions_by_subunit(self, subunit: SubUnit) -> List[Question]:
        """
        Fetches all questions associated with a specific subunit.
        """
        # Query to get questions for the specific subunit
        query = await self.db.execute(
            select(Question).filter(
                Question.subunit_id == subunit.id
            )  # Filter by subunit
        )

        questions = query.scalars().all()  # Fetch all the questions

        if not questions:
            return []  # Return an empty list if no questions found

        return questions
