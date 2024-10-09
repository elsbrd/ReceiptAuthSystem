from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo


class UserCreateSchema(BaseModel):
    name: str
    username: str
    password: str
    password_confirm: str

    @field_validator("password_confirm")
    def passwords_match(cls, password_confirm: str, validation_info: ValidationInfo):
        password = validation_info.data.get("password")
        if password != password_confirm:
            raise ValueError("Passwords do not match")
        return password_confirm


class UserLoginSchema(BaseModel):
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
