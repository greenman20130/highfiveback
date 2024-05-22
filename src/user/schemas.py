import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
class UserContact(BaseModel):
    title: str = 'Phone or email'
    value: str = '+79000000000 or pupkin@example.com'

class UserInfo(BaseModel):
    field1: str = 'string1'
    field2: str = 'string2'
    field3: str = 'string3'

class UserCreateUpdate(BaseModel):
    user_id: UUID
    user_type: str = 'login'
    login: str = 'login'
    contact_phone: list[UserContact] 
    contact_email: list[UserContact]
    additional_info: list[UserInfo]
    profile_id: UUID
    project_id: UUID
    organization_id: UUID 
    phone_verified: bool
    email_verified: bool
    password: str = 'password'

class UserRead(UserCreateUpdate):
    id: Optional[UUID] = None





class RecomendationsCreateUpdate(BaseModel): #рекомендации в случае выгорания
    id: int #PK!
    text: str

class RecomendationsRead(RecomendationsCreateUpdate):
    id: Optional[UUID] = None 