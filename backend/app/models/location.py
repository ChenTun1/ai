"""
地点模型
"""

from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Location(Base):
    """地点表（景点）"""
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # 中文名
    name_en = Column(String(255), nullable=False)  # 英文名
    continent = Column(String(50), nullable=False)  # asia | europe | americas | other
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=True)
    category = Column(String(50), default="landmark")  # landmark | nature | city
    icon = Column(String(10), default="🗺️")  # emoji图标

    # Prompt模板
    prompt_template = Column(Text, nullable=True)

    # 描述
    description = Column(Text, nullable=True)

    # 统计
    unlock_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}')>"
