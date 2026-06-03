import time
from typing import Any


def _ts() -> int:
    return int(time.time() * 1000)


def success(data: Any = None) -> dict:
    return {"code": 0, "message": "success", "data": data, "timestamp": _ts()}


def fail(code: int, message: str, data: Any = None) -> dict:
    return {"code": code, "message": message, "data": data, "timestamp": _ts()}
