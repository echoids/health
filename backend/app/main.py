from fastapi import FastAPI

app = FastAPI(title="AI健康生活助手 API")


@app.get("/health")
def health():
    return {"status": "ok"}
