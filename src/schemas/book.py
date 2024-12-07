from pydantic import BaseModel
from typing import List


class SubUnitBase(BaseModel):
    id: int
    title_en: str
    title_hi: str

    class Config:
        orm_mode = True


class UnitBase(BaseModel):
    id: int
    title_en: str
    title_hi: str
    subunits: List[SubUnitBase]

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    id: int
    title_en: str
    title_hi: str
    units: List[UnitBase]

    class Config:
        orm_mode = True
