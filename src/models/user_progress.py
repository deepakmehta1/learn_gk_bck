from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.database import Base
from src.enums.enums import QuestionStatus


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("unit.id"), nullable=False)
    sub_unit_id = Column(Integer, ForeignKey("sub_unit.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    selected_choice = Column(Integer, ForeignKey("choice.id"), nullable=True)
    is_correct = Column(Boolean, default=False, nullable=False)
    status = Column(Enum(QuestionStatus), default=QuestionStatus.READ, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="progress")
    book = relationship("Book", backref="progress")
    unit = relationship("Unit", backref="progress")
    sub_unit = relationship("SubUnit", backref="progress")
    question = relationship("Question", backref="progress")
    choice = relationship("Choice", backref="progress")

    def __repr__(self):
        return f"<UserProgress(user_id={self.user_id}, book_id={self.book_id}, unit_id={self.unit_id}, question_id={self.question_id}, status={self.status})>"
