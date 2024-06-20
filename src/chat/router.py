import datetime
import hashlib
import hmac
from http import HTTPStatus
import json
import time
from typing import Annotated, List
from uuid import UUID, uuid4
from fastapi import APIRouter, Form, Query
from fastapi.responses import Response
import requests
from fastapi.encoders import jsonable_encoder

from src.chat.schemas import ChatRead, ChatCreateUpdate, ChatUsers
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType
from src.config import COMMENT_SERVICE_URL, COMMENT_TOKEN, COMMENT_SERVICE_ID

router = APIRouter(prefix="/chat", tags=["Chat"])
_COMMENT_SERVICE_URL = f'{COMMENT_SERVICE_URL}'
_COMMENT_SERVICE_ID = f'{COMMENT_SERVICE_ID}'

@router.get("/{company_id}/{user_id}/")
async def get_chat(response: Response, company_id: UUID, user_id: UUID, 
                       presentation: str =Query('--', enum=['tree', 'flat']), 
                       scope: str = Query('--', enum=['all', 'admin', 'registered']), parent_id: int = Query(None)):
    """
    Можно запросить как все комментарии для страницы, так и только дочерние для конкретного комментария.<br>

    Параметры строки запроса:<br>

    data_type: Определяет тип запрашиваемых данных - UUID компании<br>
    item_id: Идентификатор страницы, для которой запрашиваются комментарии - UUID пользователя<br>
    Опции запроса: <br>
    presentation: Определяет вид отображения комментариев (древовидный или плоский), влияет на сортировку отдаваемых комментариев, если не указан, по умолчанию древовидный. <br>
    scope: Область видимости комментариев, если не указана, по умолчанию все. <br>
    parent_id: идентификатор родительского комментария (необязательный, если указан, выведутся дочерние комментарии) <br>
    """    
    find_chats, status = await load_objects(RegistryType.chat, filter_options = f'?search={user_id}&account_id={company_id}&meta_status=active')
    dialogs = {}
    for chat in find_chats:
        chat_id = chat['chatId']
        if user_id == chat['first_user']:
            recipient_id = chat['second_user']
        else:
            recipient_id = chat['first_user']
        key = f'{str(_COMMENT_SERVICE_ID)}{str(company_id)}{str(chat_id)}'
        signature = hmac.new(bytearray(COMMENT_TOKEN, 'utf-8'), bytearray(key, 'utf-8'), hashlib.sha1).hexdigest()
        url = f'{_COMMENT_SERVICE_URL}{_COMMENT_SERVICE_ID}/{company_id}/{chat_id}/?signature={signature}'

        if presentation != '--':
            url += f'&presentation={presentation}'
        
        if scope != '--':
            url += f'&scope={scope}'
        
        if parent_id:
            url += f'&parent_id={parent_id}'

        response = requests.get(url)
        obj = response.text
        chat = json.loads(obj)
        dialogs[recipient_id] = chat
    
    
    return dialogs

@router.post("/{company_id}/{user_id}/{recipient_id}")
async def post_chat(chat: ChatCreateUpdate, response: Response, company_id: UUID, user_id: UUID, recipient_id: UUID): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    Параметры строки запроса: <br>

    company_id: Определяет тип запрашиваемых данных - UUID компании<br>
    user_id: Идентификатор страницы, для которой запрашиваются комментарии - UUID получателя<br>
    Тело запроса: <br>
 
    comment_text: Текст комментария <br>
    user: Данные пользователя (см. схему User). Пользователь отдельной регистрации в БД не требует, при его отсутствии, он будет автоматически зарегистрирован в БД. <br>
    parent_id: Идентификатор родительского комментария (необязательный, указывается только при наличии родительского комментария) <br>
    scope: Область видимости комментариев, если не указана, по умолчанию все. <br>
    """
    data = jsonable_encoder(chat)
    
    find_chat, status = await load_objects(RegistryType.chat, filter_options = f'?search={user_id}&account_id={company_id}&meta_status=active')
    if len(find_chat) == 0:
        reg_data = {'chatId': uuid4(),
                'first_user':f'{user_id}', 
                'second_user':f'{recipient_id}'}
        reg_data_model = ChatUsers.model_validate(reg_data)
        chat_id, status = await save_object(reg_data_model, RegistryType.chat, account_id=company_id)
    
    else:
        chat_id = find_chat[0]
        chat_id = chat_id['chatId']
    
    
    key = f'{str(_COMMENT_SERVICE_ID)}{str(company_id)}{str(chat_id)}'
    data['signature'] = hmac.new(bytearray(COMMENT_TOKEN, 'utf-8'), bytearray(key, 'utf-8'), hashlib.sha1).hexdigest()
    url = f'{_COMMENT_SERVICE_URL}{_COMMENT_SERVICE_ID}/{company_id}/{chat_id}/'
    response = requests.post(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)

    return obj
    

# @router.put("/{data_type}/{item_id}/comment_id/")
# async def put_chat(chat: ChatCreateUpdate, response: Response, service_id: UUID, data_type: UUID, item_id: UUID, comment_id: UUID):
#     data = jsonable_encoder(chat)
#     url = f'{_COMMENT_SERVICE_URL}{service_id}/{data_type}/{item_id}/{comment_id}/'
#     response = requests.put(url=url, json=data)
#     obj = response.text
#     obj = json.loads(obj)

#     return obj


# @router.delete("/{data_type}/{item_id}/comment_id/")
# async def delete_chat(response: Response, service_id: UUID, data_type: UUID, item_id: UUID, comment_id: UUID):

#     url = f'{_COMMENT_SERVICE_URL}{service_id}/{data_type}/{item_id}/{comment_id}/'
#     response = requests.delete(url)
#     obj = response.text
#     obj = json.loads(obj)

#     return obj