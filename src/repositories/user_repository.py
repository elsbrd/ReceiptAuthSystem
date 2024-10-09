from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def create_user(self, name: str, username: str, password_hash: str) -> User:
        new_user = User(name=name, username=username, password_hash=password_hash)

        try:
            self.__session.add(new_user)
            self.__session.commit()
        except IntegrityError:
            self.__session.rollback()
            raise

        return new_user

    def get_user_by_username(self, username: str) -> User | None:
        return self.__session.query(User).filter(User.username == username).first()
