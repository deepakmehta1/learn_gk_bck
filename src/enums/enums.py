from enum import Enum


class QuestionStatus(str, Enum):
    READ = "read"
    SUBMITTED = "submitted"


class SubscriptionTypeEnum(str, Enum):
    FULL_SUBSCRIPTION = "full_subscription"
    BASE_SUBSCRIPTION = "base_subscription"
