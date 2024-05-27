import json

from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List

from src.poll.schemas import QuestionCreate


class TemplateObject(BaseModel):
    userId: Optional[UUID] = None
    companyId: Optional[UUID] = None
    templateName: str
    templateDescription: Optional[str] = None
    imageUrl: Optional[str] = None
    questions: List[QuestionCreate]


class TemplateRead(TemplateObject):
    id: Optional[UUID] = None

