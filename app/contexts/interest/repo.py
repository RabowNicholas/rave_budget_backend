from sqlalchemy.orm import Session

from app.contexts.interest.models import InterestFeature


class InterestRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save_feature_interest(self, i: InterestFeature) -> None:
        self.session.add(i)
        self.session.commit()
