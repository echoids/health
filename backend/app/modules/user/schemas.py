from pydantic import BaseModel


class LoginRequest(BaseModel):
    code: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str
