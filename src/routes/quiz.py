from typing import List
from fastapi import APIRouter, Depends
from src.schemas import Question, SubmitAnswerRequest, SubmitAnswerResponse
from src.services import QuizService, UserProgressService
from src.dependencies import (
    get_quiz_service,
    get_current_user,
    get_user_progress_service,
    check_user_subscription_and_preview,
)
from src.models import User

router = APIRouter()


# GET Question and Choices without the answer
@router.get("/question/{question_id}", response_model=Question)
async def get_question_with_options(
    question_id: int,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user),
    user_progress_service: UserProgressService = Depends(get_user_progress_service),
    _: bool = Depends(check_user_subscription_and_preview),
):
    # Associate the user with the progress service
    user_progress_service.associate_user(current_user)

    # Fetch the question along with its choices and related entities (book, unit, subunit)
    question = await quiz_service.get_question_with_choices(question_id)

    # Update user progress with the relevant question data
    await user_progress_service.update_user_progress(
        book_id=question["book"]["id"],
        unit_id=question["unit"]["id"],
        sub_unit_id=question["subunit"]["id"],
        question_id=question_id,
        selected_choice=None,
        is_correct=False,
        status="read",
    )

    return question


# POST Submit Answer and Check Correctness
@router.post("/question/{question_id}/submit", response_model=SubmitAnswerResponse)
async def submit_answer(
    question_id: int,
    submit_request: SubmitAnswerRequest,
    quiz_service: QuizService = Depends(get_quiz_service),
    current_user: User = Depends(get_current_user),
    user_progress_service: UserProgressService = Depends(get_user_progress_service),
    _: bool = Depends(check_user_subscription_and_preview),
):
    # Associate the user with the progress service
    user_progress_service.associate_user(current_user)

    # Fetch the question with choices
    question = await quiz_service.get_question_with_choices(question_id)

    # Submit the answer and check correctness
    choice_id = submit_request.choice_id
    submitted_response = await quiz_service.submit_answer(question_id, choice_id)

    # Update user progress with the selected choice
    _ = await user_progress_service.update_user_progress(
        book_id=question["book"]["id"],
        unit_id=question["unit"]["id"],
        sub_unit_id=question["subunit"]["id"],
        question_id=question_id,
        selected_choice=choice_id,
        is_correct=(submitted_response["correct"]),
        status="submitted",
    )

    return submitted_response


# GET API: Get questions by subunit_id
@router.get("/subunit/{subunit_id}/questions", response_model=List[Question])
async def get_questions_by_subunit(
    subunit_id: int,
    quiz_service: QuizService = Depends(get_quiz_service),
    _: User = Depends(get_current_user),
    has_access: bool = Depends(check_user_subscription_and_preview),
):
    return await quiz_service.get_questions_by_subunit_id(subunit_id)
