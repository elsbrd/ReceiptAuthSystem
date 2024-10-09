import copy
import datetime
from typing import Any, Dict

import jwt
from jwt import DecodeError
from passlib.context import CryptContext

from src.core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_auth_tokens(username: str):
    return {
        "access_token": generate_access_token(username),
        "refresh_token": generate_refresh_token(username),
        "token_type": "bearer",
    }


def generate_access_token(username: str):
    return generate_jwt_token(
        {"sub": username, "type": "access"}, settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def generate_refresh_token(username: str):
    return generate_jwt_token(
        {"sub": username, "type": "refresh"}, settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )


def generate_jwt_token(data: Dict[str, Any], expires_delta_min: int) -> str:
    to_encode = copy.deepcopy(data)
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
        minutes=expires_delta_min
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_jwt_token(token_encoded: str) -> Dict[str, Any] | None:
    try:
        return jwt.decode(
            token_encoded, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
    except DecodeError:
        return None
