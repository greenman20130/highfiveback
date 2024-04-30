from typing import Optional, List
from pydantic import BaseModel


class QuestOption(BaseModel):
    id: str
    value: Optional[str] = None
    image: Optional[str] = None


class QuestionCreate(BaseModel):
    id: int
    text: Optional[str] = None
    description: Optional[str] = None
    type: str
    required: bool
    options: List[QuestOption]


class QuestionRead(QuestionCreate):
    pass


class QuestionUpdate(BaseModel):
    id: Optional[int] = None
    text: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    required: Optional[bool] = None
    options: Optional[List[QuestOption]] = None
