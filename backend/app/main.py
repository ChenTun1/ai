"""
PetVoyageAI - AI宠物环游记 API服务
个人开发者简化版 - 使用 SQLite + 本地文件存储
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import os

from app.core.config import settings
from app.core.database import init_db

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="PetVoyageAI API",
    description="AI宠物环游记 - 让你的宠物通过AI技术环游世界",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保上传和生成目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.GENERATED_DIR, exist_ok=True)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/generated", StaticFiles(directory=settings.GENERATED_DIR), name="generated")


# 健康检查接口
@app.get("/health", tags=["System"])
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "PetVoyageAI API",
        "version": "1.0.0"
    }


# 根路由
@app.get("/", tags=["System"])
async def root():
    """API根路径"""
    return {
        "message": "欢迎使用 PetVoyageAI API",
        "docs": "/docs",
        "health": "/health"
    }


# API v1路由
from app.api.v1 import pets, photos, locations, auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(pets.router, prefix="/api/v1/pets", tags=["宠物"])
app.include_router(photos.router, prefix="/api/v1/photos", tags=["照片"])
app.include_router(locations.router, prefix="/api/v1/locations", tags=["地图"])


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "code": 50001,
            "message": "服务器内部错误",
            "data": None
        }
    )


# 启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("🚀 PetVoyageAI API 正在启动...")
    logger.info("📚 API文档: http://localhost:8000/docs")


# 关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("👋 PetVoyageAI API 正在关闭...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
