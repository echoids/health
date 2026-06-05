from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.database import get_db
from app.common.response import success
from app.common.auth import get_current_user_id
from app.modules.user import service
from app.modules.user.schemas import LoginRequest, RefreshRequest

router = APIRouter(prefix="/api/v1/user", tags=["user"])


@router.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    result = service.login(db, code=req.code)
    return success(result)


@router.post("/auth/refresh")
def refresh(req: RefreshRequest):
    result = service.refresh(req.refresh_token)
    return success(result)


@router.get("/me")
def me(user_id: int = Depends(get_current_user_id)):
    return success({"user_id": user_id})
