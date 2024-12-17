from pydantic import BaseModel
from datetime import datetime


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
    description: str


class BookDetails(BaseModel):
    id: int
    title_en: str
    title_hi: str


class ActiveSubscription(BaseModel):
    user_id: int
    subscription_id: int
    subscription_type: str
    book: BookDetails | None
    start_date: datetime
    end_date: datetime
    active: bool
