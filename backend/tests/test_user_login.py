from app.modules.user.models import User


def test_user_model_fields():
    u = User(openid="oABC123", nickname="小明")
    assert u.openid == "oABC123"
    assert u.nickname == "小明"
    assert u.is_member is False or u.is_member is None
