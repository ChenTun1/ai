"""
照片 API 路由
"""

import uuid
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.pet import Pet
from app.models.location import Location
from app.models.photo import Photo
from app.schemas.photo import (
    PhotoGenerateRequest,
    PhotoGenerateStatusResponse,
    PhotoSaveRequest,
    PhotoResponse,
)
from app.schemas.common import success_response, error_response

logger = logging.getLogger(__name__)

router = APIRouter()

# 内存中存储生成任务状态（生产环境应使用 Redis）
_generation_tasks: dict[str, dict] = {}


def _run_photo_generation(task_id: str, pet: dict, location: dict, params: dict):
    """后台执行照片生成（模拟）"""
    try:
        _generation_tasks[task_id]["status"] = "processing"
        _generation_tasks[task_id]["progress"] = 50

        # TODO: 接入硅基流动 AI 图片生成 API
        # 目前返回占位图片
        _generation_tasks[task_id]["status"] = "completed"
        _generation_tasks[task_id]["progress"] = 100
        _generation_tasks[task_id]["image_url"] = f"/generated/photo_{task_id}.png"
        _generation_tasks[task_id]["prompt"] = (
            f"A {pet['type']} ({pet.get('breed', '')}) named {pet['name']} "
            f"visiting {location['name_en']}, "
            f"{params['style']} style, {params['season']}, {params['time_of_day']}"
        )

    except Exception as e:
        logger.error(f"Photo generation failed for task {task_id}: {e}")
        _generation_tasks[task_id]["status"] = "failed"
        _generation_tasks[task_id]["error"] = str(e)


@router.post("/generate")
def generate_photo(
    req: PhotoGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """发起照片生成"""
    user_id = 1

    pet = db.query(Pet).filter(Pet.id == req.pet_id, Pet.user_id == user_id).first()
    if not pet:
        raise HTTPException(
            status_code=404,
            detail=error_response(40401, "宠物不存在"),
        )

    location = db.query(Location).filter(Location.id == req.location_id).first()
    if not location:
        raise HTTPException(
            status_code=404,
            detail=error_response(40402, "景点不存在"),
        )

    task_id = uuid.uuid4().hex

    _generation_tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "progress": 0,
        "image_url": None,
        "error": None,
        "prompt": None,
        "pet_id": req.pet_id,
        "location_id": req.location_id,
        "style": req.style,
        "season": req.season,
        "time_of_day": req.time_of_day,
        "user_id": user_id,
    }

    pet_data = {"name": pet.name, "type": pet.type, "breed": pet.breed}
    location_data = {"name": location.name, "name_en": location.name_en}
    params = {"style": req.style, "season": req.season, "time_of_day": req.time_of_day}

    background_tasks.add_task(_run_photo_generation, task_id, pet_data, location_data, params)

    return success_response(
        data={"task_id": task_id, "status": "pending"},
        message="照片生成已提交",
    )


@router.get("/generate/{task_id}")
def get_generation_status(task_id: str):
    """查询照片生成状态"""
    task = _generation_tasks.get(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=error_response(40403, "任务不存在"),
        )

    return success_response(
        data=PhotoGenerateStatusResponse(
            task_id=task["task_id"],
            status=task["status"],
            progress=task["progress"],
            image_url=task["image_url"],
            error=task["error"],
        ).model_dump()
    )


@router.post("")
def save_photo(
    req: PhotoSaveRequest,
    db: Session = Depends(get_db),
):
    """保存生成的照片"""
    task = _generation_tasks.get(req.task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=error_response(40403, "任务不存在"),
        )

    if task["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=error_response(40003, "照片尚未生成完成"),
        )

    photo = Photo(
        user_id=task["user_id"],
        pet_id=task["pet_id"],
        location_id=task["location_id"],
        image_url=task["image_url"],
        style=task["style"],
        season=task["season"],
        time_of_day=task["time_of_day"],
        prompt=task.get("prompt"),
        caption=req.caption,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    # 清理任务缓存
    _generation_tasks.pop(req.task_id, None)

    return success_response(
        data=PhotoResponse.model_validate(photo).model_dump(),
        message="照片保存成功",
    )


@router.get("")
def list_photos(
    pet_id: Optional[int] = None,
    location_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """获取照片列表"""
    user_id = 1

    query = db.query(Photo).filter(Photo.user_id == user_id)
    if pet_id is not None:
        query = query.filter(Photo.pet_id == pet_id)
    if location_id is not None:
        query = query.filter(Photo.location_id == location_id)

    total = query.count()
    photos = query.order_by(Photo.created_at.desc()).offset(skip).limit(limit).all()

    items = [PhotoResponse.model_validate(p).model_dump() for p in photos]
    return success_response(data={"items": items, "total": total})
