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
from src.config import COMMENT_SERVICE_URL, COMMENT_TOKEN, COMMENT_SERVICE_ID, BASE_REGISTRY_URL

router = APIRouter(prefix="/chat", tags=["Chat"])
_COMMENT_SERVICE_URL = f'{COMMENT_SERVICE_URL}'
_COMMENT_SERVICE_ID = f'{COMMENT_SERVICE_ID}'
_BASE_URL = f"{BASE_REGISTRY_URL}"

@router.get("/{company_id}/{user_id}/")
async def get_chat(response: Response, company_id: UUID, user_id: UUID, 
                       presentation: str =Query('--', enum=['tree', 'flat']), 
                       scope: str = Query('--', enum=['all', 'admin', 'registered']), parent_id: int = Query(None)):
    """
    Можно запросить как все сообщения для страницы.<br>

    Опции запроса: <br>
    presentation: Определяет вид отображения комментариев (древовидный или плоский), влияет на сортировку отдаваемых комментариев, если не указан, по умолчанию древовидный. <br>
    scope: Область видимости комментариев, если не указана, по умолчанию все. <br>
    parent_id: идентификатор родительского комментария (необязательный, если указан, выведутся дочерние комментарии) <br>
    """    
    find_chats, status = await load_objects(RegistryType.chat, filter_options = f'?search={user_id}&account_id={company_id}&meta_status=active')
    dialogs = []
    for chats in find_chats:
        chat_id = chats['user_id']
        # if user_id == chats['first_user']:
        #     recipient_id = chats['second_user']

        # else:
        #     recipient_id = chats['first_user']

        key = f'{str(_COMMENT_SERVICE_ID)}{str(company_id)}{str(user_id)}'
        signature = hmac.new(bytearray(COMMENT_TOKEN, 'utf-8'), bytearray(key, 'utf-8'), hashlib.sha1).hexdigest()
        url = f'{_COMMENT_SERVICE_URL}{_COMMENT_SERVICE_ID}/{company_id}/{user_id}/?signature={signature}'

        if presentation != '--':
            url += f'&presentation={presentation}'
        
        if scope != '--':
            url += f'&scope={scope}'
        
        if parent_id:
            url += f'&parent_id={parent_id}'

        response = requests.get(url)
        obj = response.text
        chat = json.loads(obj)
        len_chat = len(chat)
        if len_chat:
            chat_name = chats['chat_name']
            hr_last_check = chats['hr_last_check']
            employee_last_check = chats['employee_last_check']
            last_message = chat[len_chat - 1]
            comment_text = last_message['comment_text']
            date_created = last_message['date_created']
            anonymous = chats['anonymous']
            user_id = chats['user_id']
                
            result = {'userId': f'{user_id}',
                    'chatName' : f'{chat_name}',
                    'lastMessage' : f'{comment_text}',
                    'lastMessageDate' : f'{date_created}',
                    'employeeLastCheck' : f'{employee_last_check}',
                    'hrLastCheck' : f'{hr_last_check}',
                    'isAnonymous' : f'{anonymous}',
                    'dialogs': chat}

            dialogs.append(result)
    
    return dialogs


@router.get("/{company_id}")
async def get_chat_HR(response: Response, company_id: UUID, 
                       presentation: str =Query('--', enum=['tree', 'flat']), 
                       scope: str = Query('--', enum=['all', 'admin', 'registered']), parent_id: int = Query(None)):
    """
    Можно запросить все сообщения для HR компании<br>

    Опции запроса: <br>
    presentation: Определяет вид отображения комментариев (древовидный или плоский), влияет на сортировку отдаваемых комментариев, если не указан, по умолчанию древовидный. <br>
    scope: Область видимости комментариев, если не указана, по умолчанию все. <br>
    parent_id: идентификатор родительского комментария (необязательный, если указан, выведутся дочерние комментарии) <br>
    """    
    find_chats, status = await load_objects(RegistryType.chat, filter_options = f'?account_id={company_id}&meta_status=active')
    dialogs = []
    for chats in find_chats:
        chat_id = chats['user_id']
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
        len_chat = len(chat)
        if len_chat:
            chat_name = chats['chat_name']
            last_message = chat[len_chat - 1]
            comment_text = last_message['comment_text']
            date_created = last_message['date_created']
            hr_last_check = chats['hr_last_check']
            employee_last_check = chats['employee_last_check']
            anonymous = chats['anonymous']
            for user in chat:
                user_id = user['user']['external_id']
                if user_id != company_id:
                    break
                
            result = {'userId': f'{user_id}',
                    'chatName' : f'{chat_name}',
                    'lastMessage' : f'{comment_text}',
                    'lastMessageDate' : f'{date_created}',
                    'employeeLastCheck' : f'{employee_last_check}',
                    'hrLastCheck' : f'{hr_last_check}',
                    'isAnonymous' : f'{anonymous}',
                    'dialogs': chat}

            dialogs.append(result)
    
    
    return dialogs


@router.post("/{company_id}/{user_id}")
async def post_chat(chat: ChatCreateUpdate, response: Response, company_id: UUID, user_id: UUID): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    Параметры строки запроса: <br>

    company_id: Определяет тип запрашиваемых данных - UUID компании<br>
    user_id: Идентификатор страницы, от которой отправляется сообщение - UUID получателя<br>
    recipient_id: Идентификатор страницы, которой отправляется сообщение - UUID получателя<br>
    Тело запроса: <br>
 
    comment_text: Текст комментария <br>
    user: Данные пользователя (см. схему User). Пользователь отдельной регистрации в БД не требует, при его отсутствии, он будет автоматически зарегистрирован в БД. <br>
    parent_id: Идентификатор родительского комментария (необязательный, указывается только при наличии родительского комментария) <br>
    anonymous: Анонимность<br>
    """
    data = jsonable_encoder(chat)
    
    find_chat, status = await load_objects(RegistryType.chat, filter_options = f'?search={user_id}&account_id={company_id}&meta_status=active')

    if len(find_chat) == 0:
        if data['anonymous'] == False:
            anonymous = False
            user = data['user']
            chat_name = f"{user['first_name']} {user['last_name']}"

        elif data['anonymous'] == True:
            anonymous = True
            find_chat_name, status = await load_objects(RegistryType.chat, filter_options = f'?account_id={company_id}&meta_status=active&search=Свободный диалог')
            len_chats = len(find_chat_name)
            if len_chats > 0:
                chat_name_counter = find_chat_name[len_chats-1]['chat_name']
                chat_name_counter = chat_name_counter.replace('Свободный диалог ', '')
                chat_name_counter = int(chat_name_counter)
                chat_name_counter += 1
                chat_name = f'Свободный диалог {chat_name_counter}'

            else:
                chat_name = 'Свободный диалог 1'

        reg_data = {'user_id': f'{user_id}',
                'anonymous': anonymous,
                'chat_name': f'{chat_name}',
                'hr_last_check': f'{None}',
                'employee_last_check': f'{datetime.datetime.now()}',
                }
        
        reg_data_model = ChatUsers.model_validate(reg_data)
        chat_id, status = await save_object(reg_data_model, RegistryType.chat, account_id=company_id)
    
    else:
        chat_id = find_chat[0]
        chat_id = chat_id['user_id']
    
    if data['anonymous']:
        if data['user']['external_id'] == user_id:
            data['user']['id'] = None
            data['user']['first_name'] = None
            data['user']['last_name'] = None

    key = f'{str(_COMMENT_SERVICE_ID)}{str(company_id)}{str(user_id)}'
    data['signature'] = hmac.new(bytearray(COMMENT_TOKEN, 'utf-8'), bytearray(key, 'utf-8'), hashlib.sha1).hexdigest()
    url = f'{_COMMENT_SERVICE_URL}{_COMMENT_SERVICE_ID}/{company_id}/{user_id}/'
    response = requests.post(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.post("/{company_id}/{user_id}/read_chat")
async def read_chat(response: Response, company_id: UUID, user_id: UUID, read: str =Query('employee', enum=['HR', 'employee'])):
    url = f'{_BASE_URL}chats/?account_id={company_id}&meta_status=active&search={user_id}'
    response = requests.get(url=url)
    dialogue = json.loads(response.text)
    if len(dialogue) == 0:
        return {'error': 'No active chats found for this user'}
    
    elif len(dialogue) > 1:
        return {'error': 'More than one active chat found for this user'}
    
    dialogue = dialogue[0]
    dialogue_id = dialogue['id']
    url = f'{_BASE_URL}chat/{dialogue_id}/'
    check_time = str(datetime.datetime.now())
    if read == 'employee':
        data = {'data':{'employee_last_check': f'{check_time}'}}
    
    
    elif read == 'HR':
        data = {'data':{'hr_last_check': f'{check_time}'}}
    
    else:
        return {'error': 'Invalid read parameter'}
    
    response = requests.patch(url=url, json=data)
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