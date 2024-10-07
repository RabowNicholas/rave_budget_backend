from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.contexts.user.models import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def user_exists_by_phone(self, phone: str) -> User | None:
        return self.session.query(User).filter(User.phone == phone).first()

    def get_user_by_id(self, user_id: str) -> User:
        return self.session.query(User).filter(User.id == user_id).one()

    def create_user(self, phone: str) -> User:
        user = User(phone=phone)
        self.session.add(user)
        self.session.commit()
        return user

    def save_user(self, user: User) -> User:
        user.updated_at = datetime.now(timezone.utc)
        self.session.add(user)
        self.session.commit()
        return user
