from app.modules.user.models import User


def test_user_model_fields():
    u = User(openid="oABC123", nickname="小明")
    assert u.openid == "oABC123"
    assert u.nickname == "小明"
    assert u.is_member is False or u.is_member is None


from app.modules.user import service
from app.modules.user.models import User


def test_login_creates_new_user(db_session, mocker):
    mocker.patch.object(
        service, "wechat_code2session", return_value={"openid": "oNEW123", "unionid": None}
    )
    result = service.login(db_session, code="any_code")
    assert result["access_token"]
    assert result["refresh_token"]
    user = db_session.query(User).filter_by(openid="oNEW123").first()
    assert user is not None


def test_login_reuses_existing_user(db_session, mocker):
    db_session.add(User(openid="oOLD999"))
    db_session.commit()
    mocker.patch.object(
        service, "wechat_code2session", return_value={"openid": "oOLD999", "unionid": None}
    )
    service.login(db_session, code="any_code")
    count = db_session.query(User).filter_by(openid="oOLD999").count()
    assert count == 1
