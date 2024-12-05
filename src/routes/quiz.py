from typing import List
from fastapi import APIRouter, Depends
from src.schemas.question import Question as QuestionSchema
from src.services import QuizService
from src.dependencies import get_quiz_service

router = APIRouter()


# GET Question and Choices without the answer
@router.get("/question/{question_id}", response_model=QuestionSchema)
async def get_question_with_options(
    question_id: int, quiz_service: QuizService = Depends(get_quiz_service)
):
    return await quiz_service.get_question_with_choices(question_id)


# POST Submit Answer and Check Correctness
@router.post("/question/{question_id}/submit")
async def submit_answer_route(
    question_id: int,
    choice_id: int,
    quiz_service: QuizService = Depends(get_quiz_service),
):
    return await quiz_service.submit_answer(question_id, choice_id)


# GET API: Get questions by subunit_id
@router.get("/subunit/{subunit_id}/questions", response_model=List[QuestionSchema])
async def get_questions_by_subunit(
    subunit_id: int, quiz_service: QuizService = Depends(get_quiz_service)
):
    return await quiz_service.get_questions_by_subunit(subunit_id)
