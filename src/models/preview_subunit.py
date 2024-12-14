from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.db.database import Base
from src.models.subunit import SubUnit


class PreviewSubunit(Base):
    __tablename__ = "preview_subunit"

    id = Column(Integer, primary_key=True, index=True)
    subunit_id = Column(Integer, ForeignKey("sub_unit.id"), nullable=False)
    available_for_preview = Column(Boolean, default=True, nullable=False)

    subunit = relationship("SubUnit", back_populates="preview")

    def __repr__(self):
        return f"<PreviewSubunit(subunit_id={self.subunit_id}, available_for_preview={self.available_for_preview})>"
