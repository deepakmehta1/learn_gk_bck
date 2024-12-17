from pydantic import BaseModel


class SubmitAnswerResponse(BaseModel):
    message: str
    correct: bool
    correct_option_id: int


class CreateSubscriptionResponse(BaseModel):
    message: str


class SubscriptionType(BaseModel):
    id: int
    code: str
    name: str
    cost: int
