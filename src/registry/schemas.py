from datetime import datetime
from typing import Optional, List
from uuid import UUID
from strenum import StrEnum

from pydantic import BaseModel


class RegistryType(StrEnum):
    chat = "chat"


class RegistryMeta(BaseModel):
    """Мета данные реестра"""
    flags: int
    status: str
    internal_id: int


class RegistryRead(BaseModel):
    """Структура объекта реестра, возвращаемого get запросом."""
    id: UUID
    object_type: RegistryType
    name: str
    object_code: str
    created_date: datetime
    modified_date: datetime
    meta: RegistryMeta
    data: dict
    project_id: Optional[UUID] = None
    account_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    object_item: Optional[UUID] = None


class RegistryCreateUpdate(BaseModel):
    """Структура реестра достаточная для создания нового объекта реестра"""
    id: UUID
    object_type: RegistryType
    name: str
    object_code: str
    data: bytes
    project_id: Optional[UUID] = None
    account_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    object_item: Optional[UUID]


class RegistryMultiple(BaseModel):
    """Структура реестра при запросе multiple объекта."""
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[RegistryRead] = []
