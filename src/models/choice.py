from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base

class Choice(Base):
    __tablename__ = "choice"

    id = Column(Integer, primary_key=True, index=True)
    text_en = Column(String, index=True)
    text_hi = Column(String)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey("question.id"))

    question = relationship("Question", back_populates="choices")

    def __repr__(self):
        return f"<Choice(id={self.id}, text_en={self.text_en[:50]})>"
