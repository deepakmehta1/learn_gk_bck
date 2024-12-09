from pydantic import BaseModel
from typing import List

from pydantic import BaseModel
from typing import List, Optional


class SubUnitBase(BaseModel):
    id: int
    title_en: str
    title_hi: str
    question_count: Optional[int] = 0

    class Config:
        from_attributes = True


class UnitBase(BaseModel):
    id: int
    title_en: str
    title_hi: str
    question_count: Optional[int] = 0
    subunits: List[SubUnitBase] = []

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    id: int
    title_en: str
    title_hi: str
    units: List[UnitBase]

    class Config:
        from_attributes = True
