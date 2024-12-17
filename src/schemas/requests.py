from pydantic import BaseModel
from src.enums import SubscriptionTypeEnum


class SubmitAnswerRequest(BaseModel):
    choice_id: int


# Request model for creating a subscription
class CreateSubscriptionRequest(BaseModel):
    subscription_type: SubscriptionTypeEnum
    book_id: int | None  # Optional book_id (for base subscription)
