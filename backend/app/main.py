from fastapi import FastAPI
from app.common.exceptions import register_exception_handlers

app = FastAPI(title="AI健康生活助手 API")
register_exception_handlers(app)


@app.get("/health")
def health():
    return {"status": "ok"}
