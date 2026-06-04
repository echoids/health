from datetime import datetime, timedelta

from jose import JWTError, jwt

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
