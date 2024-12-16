from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime
from src.models import Subscription, User, SubscriptionType
from src.enums import SubscriptionTypeEnum
from typing import List, Optional


class SubscriptionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_subscription(
        self,
        user_id: int,
        book_id: Optional[int],
        subscription_type: SubscriptionTypeEnum,
    ) -> Subscription:
        """
        Create a new subscription for a user. It can be for a specific book or for all books (full subscription).
        """
        # Check if the subscription type exists in the SubscriptionType table using the enum
        subscription_type_db = await self.db.execute(
            select(SubscriptionType).filter(
                SubscriptionType.code == subscription_type.value
            )
        )
        subscription_type_db = subscription_type_db.scalars().first()

        if not subscription_type_db:
            raise HTTPException(status_code=404, detail="Subscription type not found")

        # Check if user exists
        user = await self.db.execute(select(User).filter(User.id == user_id))
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Create the new subscription
        new_subscription = Subscription(
            user_id=user_id,
            book_id=book_id,
            subscription_type_id=subscription_type_db.id,
            start_date=datetime.now(),
            active=True,
        )

        # Add to session and commit
        self.db.add(new_subscription)
        await self.db.commit()
        await self.db.refresh(new_subscription)

        return new_subscription

    async def check_user_subscription(self, user_id: int) -> Optional[Subscription]:
        """
        Check if the user has any active subscription.
        """
        result = await self.db.execute(
            select(Subscription).filter(
                Subscription.user_id == user_id, Subscription.active == True
            )
        )
        return result.scalars().first()

    async def check_user_subscription_for_book(
        self, user_id: int, book_id: int
    ) -> Optional[Subscription]:
        """
        Check if the user has an active subscription for a specific book.
        """
        result = await self.db.execute(
            select(Subscription).filter(
                Subscription.user_id == user_id,
                Subscription.book_id == book_id,
                Subscription.active == True,
            )
        )
        return result.scalars().first()

    async def get_all_user_subscriptions(self, user_id: int) -> List[Subscription]:
        """
        Fetch all subscriptions of a user.
        """
        result = await self.db.execute(
            select(Subscription).filter(Subscription.user_id == user_id)
        )
        subscriptions = result.scalars().all()

        if not subscriptions:
            raise HTTPException(
                status_code=404, detail="No subscriptions found for this user"
            )

        return subscriptions
