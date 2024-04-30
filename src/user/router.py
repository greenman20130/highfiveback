# from http import HTTPStatus
# from uuid import UUID, uuid4
# from fastapi import APIRouter
# from fastapi.responses import Response

# from src.user.schemas import UserRead, UserCreateUpdate
# from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
# from src.registry.schemas import RegistryType

# router = APIRouter(prefix="/users", tags=["User"])


# @router.post("")
# async def post_user(user: UserCreateUpdate, response: Response):
#     if user.userId is None:
#         user.userId = uuid4()
#     user_id = user.userId
#     account_id = user.companyId

#     id, status = await save_object(user, RegistryType.user,
#                                    user_id=user_id, account_id=account_id)
#     response.status_code = status
#     return id


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
