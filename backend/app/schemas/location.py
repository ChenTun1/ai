"""
景点相关 Schema
"""

from typing import Optional
from pydantic import BaseModel


class LocationResponse(BaseModel):
    id: int
    name: str
    name_en: str
    continent: str
    country: str
    city: Optional[str] = None
    category: str
    icon: str
    description: Optional[str] = None
    unlock_count: int = 0

    model_config = {"from_attributes": True}


class LocationListResponse(BaseModel):
    items: list[LocationResponse]
    total: int
