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

from src.chat.schemas import ChatRead, ChatCreateUpdate
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType
from src.config import COMMENT_SERVICE_URL, COMMENT_TOKEN, COMMENT_SERVICE_ID

router = APIRouter(prefix="/chat", tags=["Chat"])
_COMMENT_SERVICE_URL = f"{COMMENT_SERVICE_URL}"
_COMMENT_SERVICE_ID = f"{COMMENT_SERVICE_ID}"


@router.get("/{data_type}/{item_id}/")
async def get_chat(
    response: Response,
    data_type: UUID,
    item_id: UUID,
    presentation: str = Query("--", enum=["tree", "flat"]),
    scope: str = Query("--", enum=["all", "admin", "registered"]),
    parent_id: int = Query(None),
):
    """
    Можно запросить как все комментарии для страницы, так и только дочерние для конкретного комментария.<br>

    Параметры строки запроса:<br>

    service_id: Идентификатор сервиса, который запрашивает комментарии. При отсутствии сервиса в БД будет получена ошибка. Сервис должен быть предварительно зарегистрирован в БД.<br>
    data_type: Определяет тип запрашиваемых данных - UUID компании<br>
    item_id: Идентификатор страницы, для которой запрашиваются комментарии - UUID пользователя<br>
    Опции запроса: <br>
    presentation: Определяет вид отображения комментариев (древовидный или плоский), влияет на сортировку отдаваемых комментариев, если не указан, по умолчанию древовидный. <br>
    scope: Область видимости комментариев, если не указана, по умолчанию все. <br>
    parent_id: идентификатор родительского комментария (необязательный, если указан, выведутся дочерние комментарии) <br>
    """
    key = f"{str(_COMMENT_SERVICE_ID)}{str(data_type)}{str(item_id)}"
    signature = hmac.new(bytearray(COMMENT_TOKEN, "utf-8"), bytearray(key, "utf-8"), hashlib.sha1).hexdigest()
    # url += f'&signature={signature}'

    url = f"{_COMMENT_SERVICE_URL}{_COMMENT_SERVICE_ID}/{data_type}/{item_id}/?signature={signature}"
    if presentation != "--":
        url += f"&presentation={presentation}"

    if scope != "--":
        url += f"&scope={scope}"

    if parent_id:
        url += f"&parent_id={parent_id}"

    response = requests.get(url)
    obj = response.text
    chat = json.loads(obj)

    dialogue = {}
    for message in chat:
        path_user = message["user"]
        user_id = path_user["external_id"]
        if user_id not in dialogue:
            dialogue[user_id] = []

        path_dialogue = dialogue[user_id]
        path_dialogue.append(message)

    for user in dialogue:
        key = f"{str(_COMMENT_SERVICE_ID)}{str(data_type)}{str(user)}"
        signature = hmac.new(bytearray(COMMENT_TOKEN, "utf-8"), bytearray(key, "utf-8"), hashlib.sha1).hexdigest()
        url = f"{_COMMENT_SERVICE_URL}{_COMMENT_SERVICE_ID}/{data_type}/{user}/?signature={signature}"
        response = requests.get(url)
        obj = response.text
        messages = json.loads(obj)
        for message in messages:
            path_user = message["user"]
            user_id = path_user["external_id"]
            if str(item_id) == user_id:
                path_dialogue = dialogue[user]
                path_dialogue.append(message)

        path_dialogue.sort(key=lambda x: x["date_created"])

    return dialogue


@router.post("/{data_type}/{item_id}/")
async def post_chat(
    chat: ChatCreateUpdate, response: Response, data_type: UUID, item_id: UUID
):  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    Параметры строки запроса: <br>

    data_type: Определяет тип запрашиваемых данных - UUID компании<br>
    item_id: Идентификатор страницы, для которой запрашиваются комментарии - UUID получателя<br>
    Тело запроса: <br>

    comment_text: Текст комментария <br>
    user: Данные пользователя (см. схему User). Пользователь отдельной регистрации в БД не требует, при его отсутствии, он будет автоматически зарегистрирован в БД. <br>
    parent_id: Идентификатор родительского комментария (необязательный, указывается только при наличии родительского комментария) <br>
    scope: Область видимости комментариев, если не указана, по умолчанию все. <br>
    """
    data = jsonable_encoder(chat)
    key = f"{str(_COMMENT_SERVICE_ID)}{str(data_type)}{str(item_id)}"
    data["signature"] = hmac.new(bytearray(COMMENT_TOKEN, "utf-8"), bytearray(key, "utf-8"), hashlib.sha1).hexdigest()
    url = f"{_COMMENT_SERVICE_URL}{_COMMENT_SERVICE_ID}/{data_type}/{item_id}/"
    response = requests.post(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.put("/{data_type}/{item_id}/comment_id/")
async def put_chat(
    chat: ChatCreateUpdate, response: Response, service_id: UUID, data_type: UUID, item_id: UUID, comment_id: UUID
):
    data = jsonable_encoder(chat)
    url = f"{_COMMENT_SERVICE_URL}{service_id}/{data_type}/{item_id}/{comment_id}/"
    response = requests.put(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.delete("/{data_type}/{item_id}/comment_id/")
async def delete_chat(response: Response, service_id: UUID, data_type: UUID, item_id: UUID, comment_id: UUID):
    url = f"{_COMMENT_SERVICE_URL}{service_id}/{data_type}/{item_id}/{comment_id}/"
    response = requests.delete(url)
    obj = response.text
    obj = json.loads(obj)

    return obj
