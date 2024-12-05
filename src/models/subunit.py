from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base
from src.models.unit import Unit


class SubUnit(Base):
    __tablename__ = "sub_unit"

    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String)
    title_hi = Column(String)
    content_en = Column(Text)
    content_hi = Column(Text)
    subunit_number = Column(Integer)
    unit_id = Column(Integer, ForeignKey("unit.id"))

    unit = relationship("Unit", back_populates="subunits")

    questions = relationship(
        "Question",
        back_populates="subunit",
        primaryjoin="SubUnit.id == Question.subunit_id",
    )

    def __repr__(self):
        return f"<SubUnit(id={self.id}, title_en={self.title_en})>"
