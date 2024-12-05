from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.question import Question
from src.models.choice import Choice
from fastapi import HTTPException


class QuizService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_question_with_choices(self, question_id: int):
        # Fetch the question
        async with self.db.begin():
            result = await self.db.execute(
                select(Question).filter(Question.id == question_id)
            )
            question = result.scalars().first()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Fetch the choices (exclude the correct one)
        async with self.db.begin():
            choices_result = await self.db.execute(
                select(Choice).filter(Choice.question_id == question_id)
            )
            choices = choices_result.scalars().all()

        return {
            "id": question.id,
            "text_en": question.text_en,
            "text_hi": question.text_hi,
            "choices": [
                {"id": choice.id, "text_en": choice.text_en, "text_hi": choice.text_hi}
                for choice in choices
            ],
        }

    async def submit_answer(self, question_id: int, choice_id: int):
        # Fetch the question
        async with self.db.begin():
            result = await self.db.execute(
                select(Question).filter(Question.id == question_id)
            )
            question = result.scalars().first()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Fetch the choice (answer)
        async with self.db.begin():
            choice_result = await self.db.execute(
                select(Choice).filter(
                    Choice.id == choice_id, Choice.question_id == question_id
                )
            )
            choice = choice_result.scalars().first()

        if not choice:
            raise HTTPException(status_code=404, detail="Choice not found")

        # Check if the submitted choice is correct
        if choice.is_correct:
            return {"message": "Correct answer!", "correct": True}
        else:
            return {"message": "Incorrect answer. Try again!", "correct": False}

    # New method to get questions by subunit_id
    async def get_questions_by_subunit(self, subunit_id: int):
        # Fetch all questions related to the subunit
        async with self.db.begin():
            result = await self.db.execute(
                select(Question).filter(Question.subunit_id == subunit_id)
            )
            questions = result.scalars().all()

        if not questions:
            raise HTTPException(
                status_code=404, detail="No questions found for this subunit"
            )

        # Fetch the choices for each question (but not include the correct answer)
        questions_with_choices = []
        for question in questions:
            async with self.db.begin():
                choices_result = await self.db.execute(
                    select(Choice).filter(Choice.question_id == question.id)
                )
                choices = choices_result.scalars().all()

            # Add question and its choices (excluding correct answers)
            questions_with_choices.append(
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
                        for choice in choices
                    ],
                }
            )

        return questions_with_choices
