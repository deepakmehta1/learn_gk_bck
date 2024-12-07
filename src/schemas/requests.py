from pydantic import BaseModel


class SubmitAnswerRequest(BaseModel):
    choice_id: int
