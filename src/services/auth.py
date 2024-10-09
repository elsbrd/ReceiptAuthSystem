from typing import Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.security import (
    decode_jwt_token,
    generate_access_token,
    generate_auth_tokens,
    hash_password,
    verify_password,
)
from src.db.models.user import User
from src.repositories.user_repository import UserRepository


class AuthServiceException(Exception):
    pass


class DuplicateUserException(AuthServiceException):
    def __init__(self, username: str) -> None:
        self.username = username
        self.message = f"User with username `{username}` already exists"
        super().__init__(self.message)


class AuthService:
    @classmethod
    def create(cls, db_session: Session) -> "AuthService":
        return cls(UserRepository(db_session))

    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository

    def register(self, name: str, username: str, password: str) -> User:
        password_hash = hash_password(password)
        try:
            return self.__user_repository.create_user(
                name=name, username=username, password_hash=password_hash
            )
        except IntegrityError:
            raise DuplicateUserException(username)

    def login(self, username: str, password: str) -> Dict[str, str] | None:
        user = self.__user_repository.get_user_by_username(username=username)
        if not user or not verify_password(password, user.password_hash):
            return

        return generate_auth_tokens(user.username)

    def verify_access_token(self, token: str) -> User | None:
        payload = decode_jwt_token(token)

        if not payload or not payload.get("sub") or payload.get("type") != "access":
            return None

        return self.__user_repository.get_user_by_username(username=payload["sub"])

    def refresh_access_token(self, refresh_token: str) -> str | None:
        payload = decode_jwt_token(refresh_token)

        if not payload or "sub" not in payload or payload.get("type") != "refresh":
            return

        return generate_access_token(username=payload["sub"])
