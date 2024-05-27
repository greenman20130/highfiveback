from datetime import datetime

from src.question.schemas import QuestOption
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID


class Answer(BaseModel):
    questionId: int
    text: str
    answer: List[QuestOption]


class QuestResult(BaseModel):
    pollId: UUID
    templateId: UUID
    userId: UUID
    answers: List[Answer]


class QuestResultRead(QuestResult):
    id: Optional[UUID] = None
    companyId: Optional[UUID] = None
    created_date: Optional[datetime] = None
