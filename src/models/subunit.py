from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base

class SubUnit(Base):
    __tablename__ = "subunit"

    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String)
    title_hi = Column(String)
    content_en = Column(Text)
    content_hi = Column(Text)
    subunit_number = Column(Integer)
    unit_id = Column(Integer, ForeignKey("unit.id"))

    unit = relationship("Unit", back_populates="subunit")

    def __repr__(self):
        return f"<SubUnit(id={self.id}, title_en={self.title_en})>"
