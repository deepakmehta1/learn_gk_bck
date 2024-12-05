from pydantic import BaseModel
from typing import List, Optional


class BookBase(BaseModel):
    title_en: str
    title_hi: str

    class Config:
        orm_mode = True

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class UnitBase(BaseModel):
    title_en: str
    title_hi: str
    unit_number: int


class Unit(UnitBase):
    id: int
    book_id: int

    class Config:
        orm_mode = True


class SubUnitBase(BaseModel):
    title_en: str
    title_hi: str
    content_en: str
    content_hi: str
    subunit_number: int



class SubUnit(SubUnitBase):
    id: int
    unit_id: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text_en: str
    text_hi: str
    active: bool = True
    reported: bool = False


class Question(QuestionBase):
    id: int
    subunit_id: int

    class Config:
        orm_mode = True


class ChoiceBase(BaseModel):
    text_en: str
    text_hi: str
    is_correct: bool


class Choice(ChoiceBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True

class ReportedQuestionBase(BaseModel):
    explanation_en: str
    explanation_hi: str
    resolved: bool = False


class ReportedQuestion(ReportedQuestionBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True
