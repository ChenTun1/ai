"""
认证 API - 注册、登录、获取当前用户
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.common import success_response, error_response

router = APIRouter()


# ---------- Schemas ----------

class RegisterRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, pattern=r"^1\d{10}$")
    password: str = Field(..., min_length=6, max_length=32)
    username: str = Field(default="", max_length=50)


class LoginRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11)
    password: str = Field(...)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfoResponse(BaseModel):
    id: int
    phone: str
    username: str
    avatar_url: str | None
    bio: str | None
    subscription_type: str
    daily_quota_total: int
    daily_quota_used: int
    pets_count: int
    photos_count: int
    total_points: int


# ---------- Endpoints ----------

@router.post("/register")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册（手机号 + 密码）"""
    existing = db.query(User).filter(User.phone == req.phone).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该手机号已注册",
        )

    user = User(
        phone=req.phone,
        hashed_password=get_password_hash(req.password),
        username=req.username or f"用户{req.phone[-4:]}",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})

    return success_response(
        data={"access_token": token, "token_type": "bearer"},
        message="注册成功",
    )


@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    """用户登录（手机号 + 密码）"""
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    token = create_access_token(data={"sub": str(user.id)})

    return success_response(
        data={"access_token": token, "token_type": "bearer"},
        message="登录成功",
    )


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return success_response(
        data=UserInfoResponse(
            id=current_user.id,
            phone=current_user.phone,
            username=current_user.username,
            avatar_url=current_user.avatar_url,
            bio=current_user.bio,
            subscription_type=current_user.subscription_type,
            daily_quota_total=current_user.daily_quota_total,
            daily_quota_used=current_user.daily_quota_used,
            pets_count=current_user.pets_count,
            photos_count=current_user.photos_count,
            total_points=current_user.total_points,
        ).model_dump(),
    )
