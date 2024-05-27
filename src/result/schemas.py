import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class ResultCreateUpdate(BaseModel):
    pollId: UUID
    pollName: str
    templateId: UUID
    userId: UUID
    results: dict

class ResultRead(ResultCreateUpdate):
    id: Optional[UUID] = None