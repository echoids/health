def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


from app.common.response import success, fail


def test_success_response():
    r = success({"foo": "bar"})
    assert r["code"] == 0
    assert r["message"] == "success"
    assert r["data"] == {"foo": "bar"}
    assert isinstance(r["timestamp"], int)


def test_fail_response():
    r = fail(40001, "登录失败")
    assert r["code"] == 40001
    assert r["message"] == "登录失败"
    assert r["data"] is None
