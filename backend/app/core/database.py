"""
数据库连接和会话管理 - SQLite简化版
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# 确保数据目录存在
os.makedirs("./data", exist_ok=True)

# 创建SQLite引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite特定配置
    echo=settings.DEBUG  # 开发环境打印SQL
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话（依赖注入）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库（创建所有表）"""
    from app.models import user, pet, location, photo  # noqa
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库初始化完成")
