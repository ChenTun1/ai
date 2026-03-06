"""
用户模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    username = Column(String(50), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(String(500), nullable=True)

    # 订阅信息
    subscription_type = Column(String(20), default="free")  # free | premium
    subscription_expire_at = Column(DateTime, nullable=True)

    # 每日配额
    daily_quota_total = Column(Integer, default=3)  # 免费用户3次/天
    daily_quota_used = Column(Integer, default=0)
    daily_quota_reset_at = Column(DateTime, default=func.now())

    # 统计
    pets_count = Column(Integer, default=0)
    photos_count = Column(Integer, default=0)
    total_points = Column(Integer, default=0)

    # 状态
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
