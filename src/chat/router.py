from http import HTTPStatus
from uuid import UUID, uuid4
from fastapi import APIRouter
from fastapi.responses import Response

from src.chat.schemas import ChatRead, ChatCreateUpdate
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType

router = APIRouter(prefix="/chats", tags=["Chat"])


# @router.post("")
# async def post_chat(chat: ChatCreateUpdate, response: Response):
#     user_id = chat.userId

#     id, status = await save_object(chat, RegistryType.chat,
#                                    user_id=user_id)
#     response.status_code = status
#     return id


# @router.get("/{user_id}", response_model=ChatRead)
# async def get_user(user_id: UUID, response: Response):
#     """
#     Выдача сообщений пользователя.<br>
#     **user_id** Идентификатор пользователя<br>
#     **return** Сообщения ChatRead + статус **__HTTP_200_OK__**. Если пользовтель не найден - статус **__HTTP_404_NOT_FOUND__**.
#     """
#     chat, status = await load_objects(RegistryType.chat, )

#     response.status_code = status

#     return chat