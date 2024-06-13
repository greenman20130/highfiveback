from http import HTTPStatus
from uuid import UUID, uuid4
from fastapi import APIRouter
from fastapi.responses import Response

from src.company.schemas import CompanyCreateUpdate, CompanyRead
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType


router = APIRouter(prefix="/сompanies", tags=["Company"])

# @router.post("")
# async def post_company(company: CompanyCreateUpdate, response: Response):
#     if company.companyId is None:
#         company.companyId = uuid4()
#     account_id = company.companyId

#     id, status = await save_object(company, RegistryType.company,
#                                    account_id=account_id)
#     response.status_code = status
#     return id

# @router.get("/{company_id}", response_model=CompanyRead)
# async def get_company(company_id: UUID, response: Response):
#     company, status = await load_by_id(company_id, RegistryType.company)

#     response.status_code = status

#     return company

# # @router.get("/user/{company_id}", response_model=CompanyRead)
# # async def get_company(company_id: UUID, response: Response):
# #     company, status = await load_objects(company_id, RegistryType.company)

# #     response.status_code = status

# #     return company
