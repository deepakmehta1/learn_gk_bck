from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String, index=True)
    title_hi = Column(String)

    units = relationship("Unit", back_populates="book", lazy="selectin")

    def __repr__(self):
        return f"<Book(id={self.id}, title_en={self.title_en})>"
