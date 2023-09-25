from ..config import AppConfig
from ..db import User, UserRepository
from ..exceptions.common import UnauthorizedException
from ..exceptions.error_type import ErrorType


class AuthService:
    def __init__(
        self,
        config: AppConfig,
        user_repository: UserRepository,
    ) -> None:
        self.config = config
        self.user_repository = user_repository

    def new_user(self) -> User:
        return self.user_repository.create_user()

    def find_user(self, user_id: str) -> User:
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise UnauthorizedException(ErrorType.INVALID_USER)

        return user
