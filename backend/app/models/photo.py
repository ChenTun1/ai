"""
照片模型
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Photo(Base):
    """照片表"""
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    # 图片信息
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)

    # 生成参数
    style = Column(String(20), default="realistic")  # realistic | pixel | anime
    season = Column(String(20), default="summer")  # spring | summer | autumn | winter
    time_of_day = Column(String(20), default="sunset")  # sunrise | noon | sunset | night

    # 使用的Prompt
    prompt = Column(Text, nullable=True)

    # 说明文字
    caption = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Photo(id={self.id}, pet_id={self.pet_id}, location_id={self.location_id})>"


class UserUnlock(Base):
    """用户解锁记录"""
    __tablename__ = "user_unlocks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=False)
    unlocked_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<UserUnlock(user_id={self.user_id}, location_id={self.location_id})>"
