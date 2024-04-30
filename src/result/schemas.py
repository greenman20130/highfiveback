import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class ResultCreateUpdate(BaseModel):
    userId: UUID
    companyId: UUID
    sessionId: UUID
    pollId: UUID
    answerId:UUID
    result: dict

class ResultRead(ResultCreateUpdate):
    id: Optional[UUID] = None