from sqlalchemy import Column, Integer, String
from src.db.database import Base


class SubscriptionType(Base):
    __tablename__ = "subscription_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cost = Column(Integer)

    def __repr__(self):
        return f"<SubscriptionType(id={self.id}, name={self.name}, cost={self.cost})>"
