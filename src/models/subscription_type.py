from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates, relationship
from src.db.database import Base
from src.enums import SubscriptionTypeEnum


class SubscriptionType(Base):
    __tablename__ = "subscription_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(
        String,
        unique=True,
        nullable=False,
        default=SubscriptionTypeEnum.FULL_SUBSCRIPTION,
    )
    cost = Column(Integer)

    subscriptions = relationship("Subscription", back_populates="subscription_type")

    def __repr__(self):
        return f"<SubscriptionType(id={self.id}, name={self.name}, code={self.code}, cost={self.cost})>"

    @validates("code")
    def validate_code(self, key, value):
        if value not in SubscriptionTypeEnum.__members__.values():
            raise ValueError(f"{value} is not a valid subscription type")
        return value
