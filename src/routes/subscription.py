from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.models import User
from src.services import SubscriptionService
from src.dependencies import get_current_user, get_subscription_service
from src.schemas import (
    CreateSubscriptionResponse,
    CreateSubscriptionRequest,
    SubscriptionNotCompletedError,
    SubscriptionType,
)

router = APIRouter()


# POST create subscription
@router.post(
    "/create",
    response_model=CreateSubscriptionResponse,
)
async def create_subscription(
    create_subscription_request: CreateSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    # Retrieve the subscription data from the request
    subscription_type = create_subscription_request.subscription_type
    book_id = create_subscription_request.book_id

    # Call the service to create the subscription
    try:
        # Mock payment processing service (this can be replaced with actual payment logic)
        if not await mock_payment_service():
            raise SubscriptionNotCompletedError(error_code=102, detail="Payment failed")

        # Create subscription
        subscription = await subscription_service.create_subscription(
            user_id=current_user.id,
            subscription_type=subscription_type,
            book_id=book_id,
        )

        return CreateSubscriptionResponse(message="Subscription created successfully.")

    except SubscriptionNotCompletedError as e:
        # Handle the specific exception for subscription not completed
        raise SubscriptionNotCompletedError(detail=e.detail)

    except Exception as e:
        # Handle unexpected errors
        raise SubscriptionNotCompletedError(status_code=500, detail=str(e))


async def mock_payment_service() -> bool:
    """
    Mock payment service. This is where actual payment processing logic will go.
    Returns True if the payment is successful, False otherwise.
    """
    # Simulate successful payment
    return True


# GET all subscription types
@router.get("/all", response_model=List[SubscriptionType])
async def get_all_subscription_types(
    _: User = Depends(get_current_user),
    subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    """
    Fetch all subscription types (full and base subscription).
    """
    return await subscription_service.get_all_subscription_types()
