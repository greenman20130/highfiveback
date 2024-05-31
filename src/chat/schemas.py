from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class ChatUser(BaseModel):
    id: int 
    external_id: UUID
    first_name: str = None
    last_name: str = None
    user_group: str = None
class ChatCreateUpdate(BaseModel): #анонимный чат 
    comment_text: str 
    user: ChatUser
    parent_id: int = None 
    scope: str = 'all, admin, registered'

class ChatRead(ChatCreateUpdate):
    id: Optional[UUID] = None