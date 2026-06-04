import pytest
from fastapi import HTTPException

from app.common.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user_id,
)


def test_access_token_roundtrip():
    token = create_access_token(user_id=42)
    payload = decode_token(token)
    assert payload["sub"] == "42"
    assert payload["type"] == "access"


def test_refresh_token_roundtrip():
    token = create_refresh_token(user_id=42)
    payload = decode_token(token)
    assert payload["sub"] == "42"
    assert payload["type"] == "refresh"


def test_invalid_token_returns_none():
    assert decode_token("garbage.token.value") is None


def test_get_current_user_id_valid():
    token = create_access_token(user_id=7)
    assert get_current_user_id(authorization=f"Bearer {token}") == 7


def test_get_current_user_id_missing_header():
    with pytest.raises(HTTPException) as e:
        get_current_user_id(authorization=None)
    assert e.value.status_code == 401


def test_get_current_user_id_refresh_token_rejected():
    token = create_refresh_token(user_id=7)
    with pytest.raises(HTTPException) as e:
        get_current_user_id(authorization=f"Bearer {token}")
    assert e.value.status_code == 401
