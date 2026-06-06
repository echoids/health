import httpx
from sqlalchemy.orm import Session
from app.config import settings
from app.common.exceptions import BusinessError
from app.common.auth import create_access_token, create_refresh_token, decode_token
from app.modules.user.models import User

WECHAT_URL = "https://api.weixin.qq.com/sns/jscode2session"


def wechat_code2session(code: str) -> dict:
    params = {
        "appid": settings.wechat_appid,
        "secret": settings.wechat_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    resp = httpx.get(WECHAT_URL, params=params, timeout=5.0)
    data = resp.json()
    if "openid" not in data:
        raise BusinessError(40001, "微信登录失败")
    return data


def login(db: Session, code: str) -> dict:
    session_data = wechat_code2session(code)
    openid = session_data["openid"]
    user = db.query(User).filter_by(openid=openid).first()
    if user is None:
        user = User(openid=openid, unionid=session_data.get("unionid"))
        db.add(user)
        db.commit()
        db.refresh(user)
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


def refresh(refresh_token: str) -> dict:
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise BusinessError(40101, "登录已过期")
    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        raise BusinessError(40101, "登录已过期")
    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
    }
