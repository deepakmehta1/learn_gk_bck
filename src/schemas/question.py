from pydantic import BaseModel
from typing import List


class ChoiceBase(BaseModel):
    id: int
    text_en: str
    text_hi: str

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    text_en: str
    text_hi: str
    active: bool = True
    reported: bool = False


class Question(QuestionBase):
    id: int
    choices: List[ChoiceBase]

    class Config:
        from_attributes = True
