"""
宠物 API 路由
"""

import os
import logging
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.models.pet import Pet
from app.schemas.pet import PetResponse, PetListResponse
from app.schemas.common import success_response, error_response
from app.utils.file_handler import save_upload_file, create_thumbnail

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("")
async def create_pet(
    name: str = Form(..., min_length=1, max_length=50),
    type: str = Form(..., pattern="^(dog|cat|other)$"),
    breed: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """创建宠物（支持上传宠物照片）"""
    user_id = 1

    avatar_url = None
    thumbnail_url = None

    if photo and photo.filename:
        upload_dir = os.path.join(settings.UPLOAD_DIR, "pets")
        thumbnail_dir = os.path.join(settings.UPLOAD_DIR, "pets", "thumbnails")

        try:
            filename = await save_upload_file(photo, upload_dir)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=error_response(40001, str(e)),
            )

        avatar_url = f"/uploads/pets/{filename}"

        try:
            image_path = os.path.join(upload_dir, filename)
            thumb_path = os.path.join(thumbnail_dir, filename)
            create_thumbnail(image_path, thumb_path)
            thumbnail_url = f"/uploads/pets/thumbnails/{filename}"
        except Exception as e:
            logger.warning(f"缩略图生成失败，跳过: {e}")

    pet = Pet(
        user_id=user_id,
        name=name,
        type=type,
        breed=breed,
        avatar_url=avatar_url,
    )
    db.add(pet)
    db.commit()
    db.refresh(pet)

    response_data = PetResponse.model_validate(pet).model_dump()
    if thumbnail_url:
        response_data["thumbnail_url"] = thumbnail_url

    return success_response(
        data=response_data,
        message="宠物创建成功",
    )


@router.get("")
def list_pets(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """获取宠物列表"""
    user_id = 1

    query = db.query(Pet).filter(Pet.user_id == user_id)
    total = query.count()
    pets = query.order_by(Pet.created_at.desc()).offset(skip).limit(limit).all()

    items = [PetResponse.model_validate(p).model_dump() for p in pets]
    return success_response(data={"items": items, "total": total})


@router.get("/{pet_id}")
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    """获取宠物详情"""
    user_id = 1

    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.user_id == user_id).first()
    if not pet:
        raise HTTPException(
            status_code=404,
            detail=error_response(40401, "宠物不存在"),
        )

    return success_response(data=PetResponse.model_validate(pet).model_dump())
