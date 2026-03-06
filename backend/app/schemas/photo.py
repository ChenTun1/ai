"""
照片相关 Schema
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PhotoGenerateRequest(BaseModel):
    pet_id: int = Field(..., description="宠物ID")
    location_id: int = Field(..., description="景点ID")
    style: str = Field("realistic", pattern="^(realistic|pixel|anime)$", description="风格")
    season: str = Field("summer", pattern="^(spring|summer|autumn|winter)$", description="季节")
    time_of_day: str = Field("sunset", pattern="^(sunrise|noon|sunset|night)$", description="时间段")


class PhotoGenerateStatusResponse(BaseModel):
    task_id: str
    status: str  # pending | processing | completed | failed
    progress: int = 0
    image_url: Optional[str] = None
    error: Optional[str] = None


class PhotoSaveRequest(BaseModel):
    task_id: str = Field(..., description="任务ID")
    caption: Optional[str] = Field(None, max_length=500, description="说明文字")


class PhotoResponse(BaseModel):
    id: int
    user_id: int
    pet_id: int
    location_id: int
    image_url: str
    thumbnail_url: Optional[str] = None
    style: str
    season: str
    time_of_day: str
    prompt: Optional[str] = None
    caption: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PhotoListResponse(BaseModel):
    items: list[PhotoResponse]
    total: int
