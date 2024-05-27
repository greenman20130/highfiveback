from http import HTTPStatus
from uuid import UUID, uuid4
from fastapi import APIRouter, Query
from fastapi.responses import Response

from src.user.schemas import UserRead, UserCreateUpdate
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType

router = APIRouter(prefix="/user", tags=["User"])


@router.get("")
async def post_user(response: Response, profile_id: UUID = Query(None), organization_id: UUID = Query(None), project_id: UUID = Query(None)):
    filter_str = '?'
    if profile_id:
        filter_str += f'profile_id={profile_id}&'

    if organization_id:
        filter_str += f'organization_id={organization_id}&'
    
    if project_id:
        filter_str += f'project_id={project_id}'

    user, status = await load_objects(RegistryType.user, filter_options= filter_str)
    response.status_code = status
    return user


# @router.get("/{user_id}", response_model=UserRead)
# async def get_user(user_id: UUID, response: Response):
#     """
#     Выдача пользователя.<br>
#     **user_id** Идентификатор пользователя<br>
#     **return** Пользователь UserRead + статус **__HTTP_200_OK__**. Если пользовтель не найден - статус **__HTTP_404_NOT_FOUND__**.
#     """
#     user, status = await load_by_id(user_id, RegistryType.user)

#     response.status_code = status

#     return user


# # @router.get("/company/{company_id}", response_model=UserRead)
# # async def get_user_by_companyID(company_id: UUID, response: Response):
# #     """
# #     Выдача пользователя.<br>
# #     **company_id** Идентификатор компании<br>
# #     **return** Пользователь UserRead + статус **__HTTP_200_OK__**. Если пользовтель не найден - статус **__HTTP_404_NOT_FOUND__**.
# #     """
# #     user, status = await load_by_id(company_id, RegistryType.user)

# #     response.status_code = status

# #     return user
