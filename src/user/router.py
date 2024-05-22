from http import HTTPStatus
import json
from uuid import UUID, uuid4
from fastapi import APIRouter, Query
from fastapi.responses import Response
import requests
from src.config import USER_SERVICE_URL

from src.user.schemas import UserRead, UserCreateUpdate
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/user", tags=["User"])

_USER_SERVICE_URL = f'{USER_SERVICE_URL}'

@router.get("")
async def get_users(response: Response, profile_id: UUID = Query(None), organization_id: UUID = Query(None), project_id: UUID = Query(None)):
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


@router.post("")
async def post_user(user: UserCreateUpdate, response: Response):

    user, status = await save_object(user, RegistryType.user)

    response.status_code = status

    return user


@router.get("/{user_id}")
async def get_user(user_id: UUID, response: Response):
    """
    Выдача пользователя.<br>
    **user_id** Идентификатор пользователя<br>
    **return** Пользователь + статус **__HTTP_200_OK__**. Если пользовтель не найден - статус **__HTTP_404_NOT_FOUND__**.
    """

    url = _USER_SERVICE_URL
    url += f'/user/{user_id}'
    response = requests.get(url)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.put("/{user_id}")
async def put_user(user: UserCreateUpdate, user_id: UUID, response: Response):
    data = jsonable_encoder(user)
    url = _USER_SERVICE_URL
    url += f'/user/{user_id}'
    response = requests.put(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.patch("/{user_id}")
async def patch_user(user: UserCreateUpdate, user_id: UUID, response: Response):
    data = jsonable_encoder(user)
    url = _USER_SERVICE_URL
    url += f'/user/{user_id}'
    response = requests.patch(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, response: Response):

    url = _USER_SERVICE_URL
    url += f'/user/{user_id}'
    response = requests.delete(url)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.post("/hash_password")
async def post_password_to_hash(response: Response, hash_password: str = Query):

    url = _USER_SERVICE_URL
    url += f'user/hash_password?password={hash_password}'
    print(url)
    response = requests.post(url)
    obj = response.content
    obj = json.loads(obj)

    return obj


@router.post("/check_password")
async def post_password_check(response: Response, user_id: UUID = Query, password: str = Query):

    url = _USER_SERVICE_URL
    url += f'user/check_password?user_id={user_id}&password={password}'
    response = requests.post(url)
    obj = response.content

    return obj