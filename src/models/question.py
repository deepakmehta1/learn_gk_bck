from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.db.database import Base
from src.models.subunit import SubUnit
from src.models.reported_question import ReportedQuestion

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    text_en = Column(Text)
    text_hi = Column(Text)
    active = Column(Boolean, default=True)
    reported = Column(Boolean, default=False)
    subunit_id = Column(Integer, ForeignKey("sub_unit.id"))

    subunit = relationship("SubUnit", back_populates="questions")
    choices = relationship("Choice", back_populates="question")
    reported_questions = relationship("ReportedQuestion", back_populates="question", primaryjoin="Question.id == ReportedQuestion.question_id")

    def __repr__(self):
        return f"<Question(id={self.id}, text_en={self.text_en[:50]})>"
