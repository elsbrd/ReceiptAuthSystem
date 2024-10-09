from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.dependencies.db import get_db_session
from src.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_auth_service(db_session: Session = Depends(get_db_session)) -> AuthService:
    return AuthService.create(db_session)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.verify_access_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
