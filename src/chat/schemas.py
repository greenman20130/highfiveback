from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class ChatUser(BaseModel):
    id: int = None
    external_id: UUID
    first_name: str = None
    last_name: str = None
    user_group: str = None


class ChatCreateUpdate(BaseModel): #анонимный чат 
    comment_text: str 
    user: ChatUser
    parent_id: int = None 
    anonymous: bool


class ChatRead(ChatCreateUpdate):
    id: Optional[UUID] = None


class ChatUsers(BaseModel):
    user_id: UUID
    anonymous: bool
    chat_name: str
    hr_last_check: str
    employee_last_check: str