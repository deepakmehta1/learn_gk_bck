from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from src.db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    active = Column(Boolean, default=False, nullable=False)

    subscriptions = relationship("Subscription", back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email})>"
