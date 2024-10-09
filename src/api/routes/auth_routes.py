from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.db.models.user import User
from src.dependencies.auth import get_auth_service, get_current_user
from src.schemas import auth as auth_schemas
from src.schemas.auth import RefreshTokenRequest
from src.services.auth import AuthService, DuplicateUserException

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/signup")
def register_user(
    user_schema: auth_schemas.UserCreateSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    try:
        auth_service.register(
            name=user_schema.name,
            username=user_schema.username,
            password=user_schema.password,
        )
    except DuplicateUserException as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": e.message}
        )

    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/signin")
def login_user(
    sign_in_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service),
) -> Dict[str, str]:
    tokens = auth_service.login(sign_in_data.username, sign_in_data.password)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return tokens


@router.post("/refresh")
def refresh_access_token(
    refresh_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
    _: User = Depends(get_current_user),
) -> Dict[str, str]:
    access_token = auth_service.refresh_access_token(refresh_request.refresh_token)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    return {"access_token": access_token, "token_type": "bearer"}
