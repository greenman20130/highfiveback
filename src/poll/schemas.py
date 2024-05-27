import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from src.question.schemas import QuestionCreate


class PollCreateUpdate(BaseModel):
    userId: UUID
    editorId: Optional[UUID] = None
    companyId: Optional[UUID] = None 
    templateId: UUID
    adminHeading: Optional[str] = None
    adminDescription: Optional[str] = None
    pollName: str
    pollDescription: Optional[str] = None
    finalHeading: Optional[str] = None
    finalDescription: Optional[str] = None
    themeColor: str
    dateStart: Optional[datetime.datetime] = None
    dateEnd: Optional[datetime.datetime] = None
    active: bool
    questions: List[QuestionCreate]
    segmentationQuestions: Optional[List[QuestionCreate]] = None
    isSegmentTeams: Optional[bool] = None
    isSegmentExperience: Optional[bool] = None


class PollRead(BaseModel):
    id: Optional[UUID] = None
    userId: UUID
    editorId: Optional[UUID] = None
    companyId: Optional[UUID] = None
    templateId: UUID
    adminHeading: Optional[str] = None
    adminDescription: Optional[str] = None
    pollName: str
    pollDescription: Optional[str] = None
    finalHeading: Optional[str] = None
    finalDescription: Optional[str] = None
    themeColor: str
    dateStart: Optional[datetime.datetime] = None
    dateEnd: Optional[datetime.datetime] = None
    active: bool
    questions: List[QuestionCreate]
    segmentationQuestions: Optional[List[QuestionCreate]] = None
    isSegmentTeams: Optional[bool] = None
    isSegmentExperience: Optional[bool] = None


class PollByUserId(BaseModel):
    """Cтруктура, возвращаемая для просмотра списка опросов пользователя"""
    templateId: Optional[UUID] = None
    userId: Optional[UUID] = None
    companyId: Optional[UUID] = None
    pollId: UUID
    adminHeading: Optional[str] = None
    adminDescription: Optional[str] = None
    dateStart: Optional[datetime.datetime] = None
    dateEnd: Optional[datetime.datetime] = None
    resultsAmount: int = 0
