import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class UserCreateUpdate(BaseModel):
    userId: UUID = None
    companyId: UUID = None #foreignkey
    accessToken: str = None
    name: str 
    lastName: str
    city: str = None
    photo: str = None
    email: str 
    dateJoined: Optional[datetime] = None
    hashPassword: str = None
    isHr: bool 

class UserRead(UserCreateUpdate):
    id: Optional[UUID] = None




class RecomendationsCreateUpdate(BaseModel): #рекомендации в случае выгорания
    id: int #PK!
    text: str

class RecomendationsRead(RecomendationsCreateUpdate):
    id: Optional[UUID] = None 