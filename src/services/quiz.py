from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.question import Question
from src.models.choice import Choice
from fastapi import HTTPException


class QuizService:
    def __init__(self, db: AsyncSession):
        # Initializes the QuizService with the given database session
        self.db = db

    # Helper method to fetch questions with their associated choices
    async def _get_questions_with_choices(self, question_filter):
        """
        Fetches all questions and their related choices based on a filter.
        Uses `selectinload` to efficiently load choices along with questions.
        """
        async with self.db.begin():
            result = await self.db.execute(
                select(Question)
                .filter(question_filter)
                .options(selectinload(Question.choices))  # Efficiently load choices
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
                "choices": [
                    {
                        "id": choice.id,
                        "text_en": choice.text_en,
                        "text_hi": choice.text_hi,
                    }
                    for choice in question.choices  # Use pre-loaded choices
                ],
            }
            for question in questions
        ]

    # Method to get question with choices by question_id
    async def get_question_with_choices(self, question_id: int):
        """
        Fetches a single question by its ID, along with its associated choices.
        Returns the question and choices in the expected format.
        """
        questions = await self._get_questions_with_choices(Question.id == question_id)

        if not questions:
            raise HTTPException(status_code=404, detail="Question not found")

        return questions[0]  # Return the first (and only) question

    # Method to handle the submission of an answer
    async def submit_answer(self, question_id: int, choice_id: int):
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
    async def get_questions_by_subunit(self, subunit_id: int):
        """
        Fetches all questions related to a specific subunit, including their choices.
        The correct answer flag is not included in the choices.
        """
        return await self._get_questions_with_choices(Question.subunit_id == subunit_id)
