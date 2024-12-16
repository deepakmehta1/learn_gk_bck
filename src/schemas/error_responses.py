from pydantic import BaseModel


class SubscriptionError(BaseModel):
    error_code: int = 101
    detail: str = "Subscription not found"
