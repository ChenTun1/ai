"""
宠物模型
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Pet(Base):
    """宠物表"""
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)  # dog | cat | other
    breed = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)

    # AI描述（用于生成Prompt）
    ai_description = Column(String(500), nullable=True)

    # 统计
    photos_count = Column(Integer, default=0)
    locations_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Pet(id={self.id}, name='{self.name}', type='{self.type}')>"
