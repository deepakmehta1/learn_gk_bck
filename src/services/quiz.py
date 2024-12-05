from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.models.question import Question
from src.models.choice import Choice
from fastapi import HTTPException


class QuizService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Helper method to fetch questions with choices
    async def _get_questions_with_choices(self, question_filter):
        # Fetch all questions and their choices related to the filter
        async with self.db.begin():
            result = await self.db.execute(
                select(Question)
                .filter(question_filter)
                .options(selectinload(Question.choices))  # Efficiently load choices
            )
            questions = result.scalars().all()

        if not questions:
            raise HTTPException(status_code=404, detail="No questions found")

        # Build the response for each question with its choices
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
        # Fetch the question and its choices
        questions = await self._get_questions_with_choices(Question.id == question_id)

        if not questions:
            raise HTTPException(status_code=404, detail="Question not found")

        return questions[0]  # Return the first (and only) question

    # Method to submit an answer
    async def submit_answer(self, question_id: int, choice_id: int):
        # Fetch the question and its choices
        questions = await self._get_questions_with_choices(Question.id == question_id)

        if not questions:
            raise HTTPException(status_code=404, detail="Question not found")

        # Find the choice within the pre-loaded choices
        question = questions[0]
        choice = next((ch for ch in question["choices"] if ch["id"] == choice_id), None)

        if not choice:
            raise HTTPException(status_code=404, detail="Choice not found")

        # Check if the submitted choice is correct (assuming 'is_correct' is part of your choice model)
        if choice["is_correct"]:
            return {"message": "Correct answer!", "correct": True}
        else:
            return {"message": "Incorrect answer. Try again!", "correct": False}

    # Method to get questions by subunit_id with choices (without correct answer)
    async def get_questions_by_subunit(self, subunit_id: int):
        # Fetch questions with choices related to the subunit
        return await self._get_questions_with_choices(Question.subunit_id == subunit_id)
