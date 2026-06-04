from unittest.mock import MagicMock
from app.common import redis_client


def test_get_redis_returns_client(mocker):
    fake = MagicMock()
    mocker.patch.object(redis_client, "_pool", fake)
    client = redis_client.get_redis()
    assert client is not None
