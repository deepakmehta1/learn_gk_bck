from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.db.database import Base
from src.models.subscription_type import SubscriptionType


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(
        Integer, ForeignKey("book.id"), nullable=True
    )  # Can be None for full subscription
    subscription_type_id = Column(
        Integer, ForeignKey("subscription_type.id"), nullable=False
    )
    start_date = Column(DateTime, default=datetime.now(timezone.utc))
    end_date = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscriptions", lazy="selectin")
    book = relationship("Book", back_populates="subscriptions", lazy="selectin")
    subscription_type = relationship(
        "SubscriptionType", back_populates="subscriptions", lazy="selectin"
    )

    def __repr__(self):
        return f"<Subscription(user_id={self.user_id}, book_id={self.book_id}, active={self.active}, subscription_type={self.subscription_type.name})>"
