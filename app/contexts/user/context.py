from app.contexts.user.models import User
from app.contexts.user.repo import UserRepository


class UserContext:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def user_exists_by_phone(self, phone: str) -> User | None:
        return self.repository.user_exists_by_phone(phone)

    def create_user(self, phone: str) -> User:
        return self.repository.create_user(phone)

    def onboard_user(self, user: User, name: str) -> User:
        user.name = name
        return self.repository.save_user(user)
