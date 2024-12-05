from pydantic import BaseModel


class ChoiceBase(BaseModel):
    text_en: str
    text_hi: str
    is_correct: bool

    class Config:
        from_attributes = True


class Choice(ChoiceBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True
