from app.contexts.interest.models import InterestFeature
from app.contexts.interest.repo import InterestRepository


class InterestContext:
    def __init__(self, repository: InterestRepository) -> None:
        self.repository = repository

    def add_feature_interest(
        self,
        user_id: str,
        name: str,
    ) -> None:
        i = InterestFeature(user_id=user_id, name=name)
        self.repository.save_feature_interest(i)
