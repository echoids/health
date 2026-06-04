from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Header, HTTPException

from app.config import settings


def _create_token(user_id: int, token_type: str, expire_days: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "exp": datetime.utcnow() + timedelta(days=expire_days),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: int) -> str:
    return _create_token(user_id, "access", settings.access_token_expire_days)


def create_refresh_token(user_id: int) -> str:
    return _create_token(user_id, "refresh", settings.refresh_token_expire_days)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None


def get_current_user_id(authorization: str | None = Header(default=None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="缺少认证信息")
    token = authorization[len("Bearer "):]
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="认证失效")
    return int(payload["sub"])
