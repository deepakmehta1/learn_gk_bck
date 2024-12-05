from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from src.db.database import Base
from sqlalchemy.orm import relationship

class ReportedQuestion(Base):
    __tablename__ = "reported_question"

    id = Column(Integer, primary_key=True, index=True)
    explanation_en = Column(Text)
    explanation_hi = Column(Text)
    resolved = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("question.id"))

    question = relationship("Question", back_populates="reported_question")

    def __repr__(self):
        return f"<ReportedQuestion(id={self.id}, question_id={self.question_id})>"
