from http import HTTPStatus
import json
from uuid import UUID, uuid4
from fastapi import APIRouter, Query, FastAPI
from fastapi.responses import Response
import requests
from src.config import USER_SERVICE_URL

from src.user_information.schemas import ProfileCreateUpdate
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/profile", tags=["Profile"])

_USER_SERVICE_URL = f'{USER_SERVICE_URL}'

@router.get("")
async def get_profile(response: Response, profile_id: UUID = Query(None), account_id: UUID = Query(None), project_id: UUID = Query(None), first_name: str = Query(None), 
                    middle_name: str = Query(None), last_name: str = Query(None), contact_phone: str = Query(None), contact_email: str = Query(None), exact_search: bool = Query(None)):
    url = str(_USER_SERVICE_URL) + 'profiles?'
    if profile_id:
        url += f'profile_id={profile_id}'

    if account_id:
        url += f'&account_id={account_id}'

    if project_id:
        url += f'&project_id={project_id}'
    
    if first_name:
        url += f'&first_name={first_name}'
    
    if middle_name:
        url += f'&middle_name={middle_name}'
    
    if last_name:
        url += f'&last_name={last_name}'

    if contact_phone:
        url += f'&contact_phone={contact_phone}'

    if contact_email:
        url += f'&contact_email={contact_email}'

    if exact_search:
        url += f'&exact_search={exact_search}'  

    response = requests.get(url)
    profiles = json.loads(response.content)
    return profiles


@router.post("")
async def post_profile(profile: ProfileCreateUpdate, response: Response):

    data = jsonable_encoder(profile)
    url = f'{_USER_SERVICE_URL}profile'
    response = requests.post(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)

    return obj



@router.get("/{profile_id}")
async def get_profile(profile_id: UUID, response: Response):

    url = _USER_SERVICE_URL
    url += f'/profile/{profile_id}'
    response = requests.get(url)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.put("/{profile_id}")
async def put_profile(profile: ProfileCreateUpdate, profile_id: UUID, response: Response):
    data = jsonable_encoder(profile)
    url = _USER_SERVICE_URL
    url += f'/profile/{profile_id}'
    response = requests.put(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)

    return obj


@router.patch("/{profile_id}")
async def patch_profile(profile: ProfileCreateUpdate, profile_id: UUID, response: Response):
    data = jsonable_encoder(profile)
    url = _USER_SERVICE_URL
    url += f'/profile/{profile_id}'
    response = requests.patch(url=url, json=data)
    obj = response.text
    obj = json.loads(obj)
    
    return obj


@router.delete("/{profile_id}")
async def delete_profile(profile_id: UUID, response: Response):

    url = _USER_SERVICE_URL
    url += f'/profile/{profile_id}'
    response = requests.delete(url)
    obj = response.text
    obj = json.loads(obj)

    return obj
