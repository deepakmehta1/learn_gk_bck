from pydantic import BaseModel
from fastapi import HTTPException


class SubscriptionError(BaseModel):
    error_code: int = 101
    detail: str = "Subscription not found"


class SubscriptionNotCompletedError(HTTPException):
    def __init__(
        self, error_code: int = 102, detail: str = "Subscription not completed"
    ):
        self.status_code = 404
        self.error_code = error_code
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)
