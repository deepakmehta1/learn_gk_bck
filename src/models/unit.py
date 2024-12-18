from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from src.db.database import Base
from src.models.book import Book


class Unit(Base):
    __tablename__ = "unit"

    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String)
    title_hi = Column(String)
    unit_number = Column(Integer)
    book_id = Column(Integer, ForeignKey("book.id"))

    book = relationship("Book", back_populates="units", lazy="selectin")
    subunits = relationship("SubUnit", back_populates="unit", lazy="selectin")

    def __repr__(self):
        return f"<Unit(id={self.id}, title_en={self.title_en})>"
