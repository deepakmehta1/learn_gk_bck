from fastapi import APIRouter, Depends, HTTPException
from src.models import User
from src.services import UserProgressService, QuizService, SubscriptionService
from src.schemas import UserProgressResponse, ActiveSubscription
from src.dependencies import (
    get_user_progress_service,
    get_current_user,
    get_quiz_service,
    get_subscription_service,
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
    # Associate the user with the progress service
    user_progress_service.associate_user(current_user)

    # Call service to fetch user progress
    user_progress = await user_progress_service.get_user_progress_by_type(
        quiz_service, type, type_id
    )

    if not user_progress:
        raise HTTPException(status_code=404, detail="No progress found")

    return user_progress


# GET User's active subscription
@router.get("/active-subscription", response_model=ActiveSubscription)
async def get_active_subscription(
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    """
    Get the active subscription for the current user.
    """
    # Fetch the active subscription for the user
    active_subscription = await subscription_service.get_active_subscription(
        current_user.id
    )

    book = active_subscription.book
    book_data = {
        "id": book.id,
        "title_en": book.title_en,
        "title_hi": book.title_hi,
    }

    return ActiveSubscription(
        user_id=current_user.id,
        subscription_id=active_subscription.id,
        subscription_type=active_subscription.subscription_type.code,
        book=book_data,
        start_date=active_subscription.start_date,
        end_date=active_subscription.end_date,
        active=active_subscription.active,
    )
