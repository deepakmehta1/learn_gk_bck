from pydantic import BaseModel


class SubmitAnswerResponse(BaseModel):
    message: str
    correct: bool
    correct_option_id: int


class CreateSubscriptionResponse(BaseModel):
    message: str
