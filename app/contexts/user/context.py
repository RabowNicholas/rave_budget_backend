from app.contexts.user.models import User
from app.contexts.user.repo import UserRepository


class UserUpdateData:
    name: str


class UserContext:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def user_exists_by_phone(self, phone: str) -> User | None:
        return self.repository.user_exists_by_phone(phone)

    def get_user_by_id(self, user_id: str) -> User:
        return self.repository.get_user_by_id(user_id)

    def create_user(self, phone: str) -> User:
        return self.repository.create_user(phone)

    def onboard_user(self, user: User, name: str) -> User:
        user.name = name
        return self.repository.save_user(user)

    def update_user(self, user_id: str, update_data: UserUpdateData) -> User:
        user = self.get_user_by_id(user_id)
        user.name = update_data.name
        return self.repository.save_user(user)
