from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel


class CompanyCreateUpdate(BaseModel):
    companyId: UUID = None
    name: str
    employment: str
    website: str = None
    city: str

class CompanyRead(CompanyCreateUpdate):
    id: Optional[UUID] = None