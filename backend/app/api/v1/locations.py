"""
景点 API 路由
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.location import Location
from app.schemas.location import LocationResponse
from app.schemas.common import success_response, error_response

router = APIRouter()


@router.get("")
def list_locations(
    continent: Optional[str] = None,
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """获取景点列表（支持筛选）"""
    query = db.query(Location)

    if continent:
        query = query.filter(Location.continent == continent)
    if category:
        query = query.filter(Location.category == category)
    if keyword:
        query = query.filter(
            Location.name.contains(keyword) | Location.name_en.contains(keyword)
        )

    total = query.count()
    locations = query.order_by(Location.id).offset(skip).limit(limit).all()

    items = [LocationResponse.model_validate(loc).model_dump() for loc in locations]
    return success_response(data={"items": items, "total": total})


@router.get("/{location_id}")
def get_location(location_id: int, db: Session = Depends(get_db)):
    """获取景点详情"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=404,
            detail=error_response(40404, "景点不存在"),
        )

    return success_response(data=LocationResponse.model_validate(location).model_dump())
