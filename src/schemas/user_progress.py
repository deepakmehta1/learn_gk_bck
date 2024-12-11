from pydantic import BaseModel
from typing import Optional, List


class UserProgressBase(BaseModel):
    user_id: int
    book_id: Optional[int] = None
    unit_id: Optional[int] = None
    sub_unit_id: Optional[int] = None
    question_id: Optional[int] = None
    selected_choice: Optional[int] = None
    is_correct: bool
    status: str

    class Config:
        from_attributes = True


class RecentQuestionDetails(BaseModel):
    unit_id: int
    sub_unit_id: int
    question_id: int
    status: str


class UserProgressResponse(BaseModel):
    total_questions: int
    total_questions_attempted: int
    total_questions_correct: int
    accuracy: float
    recent_question_details: List[RecentQuestionDetails]
