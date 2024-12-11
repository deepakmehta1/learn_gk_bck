from fastapi import APIRouter, Depends, HTTPException
from src.models import User
from src.services import UserProgressService, QuizService
from src.schemas.user_progress import UserProgressResponse
from src.dependencies import (
    get_user_progress_service,
    get_current_user,
    get_quiz_service,
)

router = APIRouter()


@router.get("/progress", response_model=UserProgressResponse)
async def get_user_progress_by_type(
    type: str,
    type_id: int,
    quiz_service: QuizService = Depends(get_quiz_service),
    user_progress_service: UserProgressService = Depends(get_user_progress_service),
    current_user: User = Depends(get_current_user),
):
    """
    Get all user progress based on the type (book, unit, or subunit) and the respective ID.
    """
    # Call service to fetch user progress
    user_progress = await user_progress_service.get_user_progress_by_type(
        quiz_service, type, type_id
    )

    if not user_progress:
        raise HTTPException(status_code=404, detail="No progress found")

    return user_progress
