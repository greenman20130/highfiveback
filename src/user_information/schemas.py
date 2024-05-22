import datetime
from typing import Optional, List, Union
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
class ProfileContact(BaseModel):
    title: str = 'Phone or email'
    value: str = '+79000000000 or pupkin@example.com'

class ProjectInfo(BaseModel):
    field1: str = 'string1'
    field2: str = 'string2'
    field3: str = 'string3'

class ProfileCreateUpdate(BaseModel):
    profile_id: UUID
    profile_type: str = 'anonymous or person'
    first_name: str = 'Green'
    middle_name: str = 'Man'
    birth_date: str = '04.03.1382'
    sex: str = 'Male or female'
    contact_phone: list[ProfileContact] 
    contact_email: list[ProfileContact]
    photo_main: str = 'https://photo.ru/1234'
    photo_small: str = 'https://photo.ru/1234/small'
    project_info: Union[ProjectInfo]
    project_id: UUID
    account_id: UUID
    

class ProfileRead(ProfileCreateUpdate):
    id: Optional[UUID] = None





class RecomendationsCreateUpdate(BaseModel): #рекомендации в случае выгорания
    id: int #PK!
    text: str

class RecomendationsRead(RecomendationsCreateUpdate):
    id: Optional[UUID] = None 