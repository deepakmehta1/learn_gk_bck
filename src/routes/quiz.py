# src/routes/quiz.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db.database import get_db
from src.models.question import Question
from src.models.choice import Choice
from src.schemas.question import Question as QuestionSchema

router = APIRouter()

@router.get("/question/{question_id}", response_model=QuestionSchema)
async def get_question_with_options(
    question_id: int, db: AsyncSession = Depends(get_db)
):
    # Fetch the question
    async with db.begin():
        result = await db.execute(
            select(Question).filter(Question.id == question_id)
        )
        question = result.scalars().first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Fetch choices (exclude the correct one)
    async with db.begin():
        choices_result = await db.execute(
            select(Choice).filter(Choice.question_id == question_id)
        )
        choices = choices_result.scalars().all()

    return {
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

@router.post("/question/{question_id}/submit")
async def submit_answer(
    question_id: int, choice_id: int, db: AsyncSession = Depends(get_db)
):
    # Fetch the question
    async with db.begin():
        result = await db.execute(
            select(Question).filter(Question.id == question_id)
        )
        question = result.scalars().first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Fetch the choice (answer)
    async with db.begin():
        choice_result = await db.execute(
            select(Choice).filter(Choice.id == choice_id, Choice.question_id == question_id)
        )
        choice = choice_result.scalars().first()

    if not choice:
        raise HTTPException(status_code=404, detail="Choice not found")

    # Check if the submitted choice is correct
    if choice.is_correct:
        return {"message": "Correct answer!", "correct": True}
    else:
        return {"message": "Incorrect answer. Try again!", "correct": False}
