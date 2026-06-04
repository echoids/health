from app.common.auth import create_access_token, create_refresh_token, decode_token


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
