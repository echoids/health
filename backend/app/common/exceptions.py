from fastapi import Request
from fastapi.responses import JSONResponse
from app.common.response import fail


class BusinessError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


def register_exception_handlers(app):
    @app.exception_handler(BusinessError)
    async def business_error_handler(request: Request, exc: BusinessError):
        return JSONResponse(status_code=200, content=fail(exc.code, exc.message))
