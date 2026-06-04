from fastapi import FastAPI
from app.common.exceptions import register_exception_handlers
from app.modules.user.router import router as user_router

app = FastAPI(title="AI健康生活助手 API")
register_exception_handlers(app)
app.include_router(user_router)


@app.get("/health")
def health():
    return {"status": "ok"}
