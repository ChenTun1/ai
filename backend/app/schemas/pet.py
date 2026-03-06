"""
宠物相关 Schema
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class PetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="宠物名称")
    type: str = Field(..., pattern="^(dog|cat|other)$", description="宠物类型")
    breed: Optional[str] = Field(None, max_length=100, description="品种")


class PetResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    breed: Optional[str] = None
    avatar_url: Optional[str] = None
    ai_description: Optional[str] = None
    photos_count: int = 0
    locations_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PetListResponse(BaseModel):
    items: list[PetResponse]
    total: int
