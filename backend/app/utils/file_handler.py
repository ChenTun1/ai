"""
文件上传与图片处理工具
"""

import os
import uuid
import logging
from pathlib import Path

from fastapi import UploadFile
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}


def generate_unique_filename(original_filename: str) -> str:
    """生成唯一文件名（UUID + 原始扩展名）"""
    ext = "jpg"
    if original_filename and "." in original_filename:
        ext = original_filename.rsplit(".", 1)[-1].lower()
    return f"{uuid.uuid4().hex}.{ext}"


def validate_image_file(file: UploadFile) -> bool:
    """验证是否为允许的图片文件（jpg, jpeg, png）"""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return False

    if file.filename:
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            return False

    return True


async def save_upload_file(file: UploadFile, directory: str) -> str:
    """
    保存上传文件到指定目录。

    Args:
        file: FastAPI UploadFile 对象
        directory: 目标存储目录（绝对路径或相对路径）

    Returns:
        保存后的文件名

    Raises:
        ValueError: 文件类型不合法或文件过大
        IOError: 文件写入失败
    """
    if not validate_image_file(file):
        raise ValueError("不支持的图片格式，仅支持 JPG/JPEG/PNG")

    content = await file.read()

    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise ValueError(
            f"图片大小超过限制（最大 {settings.MAX_UPLOAD_SIZE // (1024 * 1024)}MB）"
        )

    os.makedirs(directory, exist_ok=True)

    filename = generate_unique_filename(file.filename or "upload.jpg")
    filepath = os.path.join(directory, filename)

    with open(filepath, "wb") as f:
        f.write(content)

    logger.info(f"文件已保存: {filepath} ({len(content)} bytes)")
    return filename


def create_thumbnail(
    image_path: str, thumbnail_path: str, size: tuple[int, int] = (300, 300)
) -> None:
    """
    为图片创建缩略图。

    Args:
        image_path: 原图的绝对路径
        thumbnail_path: 缩略图保存路径
        size: 缩略图尺寸 (宽, 高)

    Raises:
        FileNotFoundError: 原图文件不存在
        IOError: 图片处理失败
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"原图文件不存在: {image_path}")

    thumbnail_dir = os.path.dirname(thumbnail_path)
    os.makedirs(thumbnail_dir, exist_ok=True)

    with Image.open(image_path) as img:
        img.thumbnail(size, Image.Resampling.LANCZOS)
        img.save(thumbnail_path)

    logger.info(f"缩略图已生成: {thumbnail_path}")
