from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class ChatCreateUpdate(BaseModel): #анонимный чат 
    messageId: UUID = None
    text: str
    userId: UUID = None #foreignkey
    recipientId: UUID = None #foreignkey
    time: Optional[datetime] = None

class ChatRead(ChatCreateUpdate):
    id: Optional[UUID] = None