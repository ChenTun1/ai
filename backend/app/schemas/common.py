"""
统一响应格式
"""

from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None


def success_response(data: Any = None, message: str = "success") -> dict:
    return {"code": 0, "message": message, "data": data}


def error_response(code: int, message: str, data: Any = None) -> dict:
    return {"code": code, "message": message, "data": data}
