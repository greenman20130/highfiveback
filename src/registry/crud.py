"""
Работа с реестрами
"""
import json
from uuid import UUID, uuid4
from typing import Any

from src.config import BASE_REGISTRY_URL, POLL_SERVICE_URL, USER_SERVICE_URL
from src.registry.schemas import RegistryType, RegistryCreateUpdate, RegistryRead, RegistryMultiple
from src.registry.service_data import REGISTRY_SETTING, _MANY, _STRUCT, _ONCE
from src.poll.schemas import *
from src.answer.schemas import *

from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK, HTTP_201_CREATED
import requests

_BASE_URL = f"{BASE_REGISTRY_URL}"

_POLL_SERVICE_URL = f"{POLL_SERVICE_URL}"  # url готового сервиса опросника
_POLL_SERVICE_TYPE = [RegistryType.poll, RegistryType.answer, RegistryType.template] # типы опросника

_USER_SERVICE_URL = f"{USER_SERVICE_URL}"
_USER_SERVICE_TYPE = [RegistryType.user,] # типы центра пользователей
second_id = None

_METHOD_TYPE = {'polls_by_company':{'struct':None, 'url':'/company',},
                'polls_by_user':{'struct':None, 'url':'/user',},
                'polls_by_template':{'struct':None, 'url':'/template',},
                'result_by_answer':{'struct':None, 'url':None},
                'answers_by_company_id':{'struct':None, 'url':None},
                }


# class UUIDEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, UUID):
#             return str(obj)
#         return json.JSONEncoder.default(self, obj)

async def load_objects(obj_type: RegistryType, filter_options: str = None) -> (
        tuple[None, Any] | tuple[str, int] | tuple[None, int]):
    """Чтение списка объектов из реестра

    Returns:
        object: 
    """
    setting = REGISTRY_SETTING.get(obj_type)

    if obj_type in _POLL_SERVICE_TYPE:
        url = _POLL_SERVICE_URL

    elif obj_type in _USER_SERVICE_TYPE:
        url = _USER_SERVICE_URL

    else:
        url = _BASE_URL

    url += setting[_MANY]

    if filter_options is not None:
        url += filter_options
    
    response = requests.get(url)

    if obj_type in _POLL_SERVICE_TYPE or _USER_SERVICE_TYPE:
        result = (json.loads(response.text), response.status_code)
        return result

    if response.status_code == HTTP_200_OK:
        result_list = []

        try:
            list_obj = json.loads(response.content)

            for obj in list_obj:
                reg = RegistryRead.model_validate(obj)
                object_dump = setting[_STRUCT].model_validate(reg.data)

                if hasattr(object_dump, 'id'):
                    object_dump.id = obj['id']

                if hasattr(object_dump, 'companyId'):
                    object_dump.companyId = obj['account_id']

                if hasattr(object_dump, 'userId'):
                    object_dump.userId = obj['user_id']

                if hasattr(object_dump, 'created_date'):
                    object_dump.created_date = obj['created_date']

                result_list.append(object_dump.model_dump())
            result = (result_list, response.status_code)
        except ValidationError:
            result = (None, HTTP_422_UNPROCESSABLE_ENTITY)

    else:
        result = (None, response.status_code)

    return result


async def load_counts(obj_type: RegistryType, *, limit: int = 1, filter_options: str = None):
    setting = REGISTRY_SETTING.get(obj_type)

    if obj_type in _POLL_SERVICE_TYPE:
        url = _POLL_SERVICE_URL

    else:
        url = _BASE_URL
    url += setting[_MANY]

    if filter_options is not None:
        url += filter_options + f"&limit={limit}"

    else:
        url += f"?limit={limit}"

    response = requests.get(url)

    if response.status_code == HTTP_200_OK:
        list_obj = json.loads(response.content)
        reg = RegistryMultiple.model_validate(list_obj)
        return (reg.count, response.status_code)

    return (0, response.status_code)


async def load_by_id(obj_id: UUID, obj_type: RegistryType, method_type: str = None, second_id: UUID = None, specific_url: str = None):
    """
    Loads an object from the registry.

    Args:
        obj_id: The ID of the object to load.
        obj_type: The type of the object to load.
        method_type: The method to use for loading the object.

    Returns:
        A tuple containing the loaded object and its status code.
    """

    # Retrieve the registry setting for the given object type.
    setting = REGISTRY_SETTING.get(obj_type)

    # Check if the object type is supported by the service.
    if obj_type in _POLL_SERVICE_TYPE:
        # Construct the URL for fetching the object.
        url = _POLL_SERVICE_URL
        if specific_url:
            url += specific_url

        else:
            url += setting[_MANY] + f"{obj_id}"
            struct = setting[_STRUCT]

        # Check if a method type is specified.
        if method_type is not None:
            # Get the method configuration.
            method_type = _METHOD_TYPE[method_type]

            # Append the method URL to the URL.
            # if second_id is not None:
            #     full_url = method_type.get('url')
            #     url = f'{url+full_url[0]}'
            
            #else:
            if method_type.get('url') is not None:
                url += method_type.get('url')

            # Check if a 'struct' parameter is defined.
            if 'struct' in method_type:
                # Validate the 'struct' parameter.
                struct = method_type['struct']
                if struct is None:
                    # Fetch the object from the service.
                    response = requests.get(url)
                    obj = response.text
                    obj = json.loads(obj)
                    # Return the object and its status code.
                    result = (obj, response.status_code)
                    return result

        # Fetch the object from the service.
        response = requests.get(url)
        obj = response.text
        obj = json.loads(obj)

        # Validate the object against its defined structure.
        obj = struct.model_validate(obj)

        # Return the object and its status code.
        result = (obj, response.status_code)
        return result
        

    else:
        url = _BASE_URL
        url += setting[_ONCE] + f"{obj_id}/"
        response = requests.get(url)

    
    if response.status_code == HTTP_200_OK:

        try:
            reg = RegistryRead.model_validate_json(response.content)
            obj = setting[_STRUCT].model_validate(reg.data)
            obj.id = reg.id
            result = (obj, response.status_code)

        except ValidationError:
            result = (None, HTTP_422_UNPROCESSABLE_ENTITY)

    else:
        result = (None, response.status_code)

    return result


async def save_object(data_to_save, obj_type: RegistryType, *,
                      project_id=None,
                      account_id=None,
                      user_id=None,
                      object_item=None):
    """
    Сохранение данных в реестр.
    :data_to_save: объект для сохранения в реестр
    :obj_type: тип сохраняемого объекта (одно из значений ObjectType)
    :return: множество (id, status_code) - id созданного объекта, статус-код операции
             если объект не проходит валидацию - None ошибка 422 и пустой результат
    """
    setting = REGISTRY_SETTING.get(obj_type)

    if obj_type in _POLL_SERVICE_TYPE:
        url = _POLL_SERVICE_URL
        url += setting[_MANY]
        if _POLL_SERVICE_TYPE == RegistryType.poll or RegistryType.answer:
            url = url[0:-1]

        data = jsonable_encoder(data_to_save)
        response = requests.post(url=url, json=data)

    else:
        url = _BASE_URL
        url += setting[_ONCE]

        uuid_reg = uuid4()
        
        data = RegistryCreateUpdate(
            object_type=obj_type,
            name=f"{obj_type}_{uuid_reg}",
            object_code=f"{uuid_reg}",
            project_id=project_id,
            account_id=account_id,
            user_id=user_id,
            object_item=object_item,
            data=data_to_save.model_dump_json(),
        )
        response = requests.post(url, data=data.model_dump())
    id = None

    if response.status_code == HTTP_201_CREATED:
        id = json.loads(response.content)["id"]

    return {"id": id}, response.status_code


async def update_by_id(obj_id: UUID, data_to_update, obj_type: RegistryType, *,
                       project_id=None,
                       account_id=None,
                       user_id=None,
                       object_item=None):
    """
    Обновление данных об объекте
    Args:
        obj_id: идентификатор обновляемого объекта
        data_to_update: данные для обновления
        obj_type: тип обновляемого объекта в реестре
        project_id:
        account_id:
        user_id:
        object_item:
    Returns:
        код выполнения операции
    """
    setting = REGISTRY_SETTING[obj_type]

    if obj_type in _POLL_SERVICE_TYPE:
        url = _POLL_SERVICE_URL + setting.get(_MANY) + f"{obj_id}"


        data = jsonable_encoder(data_to_update)

        
        response = requests.put(url=url, json=data)
        return response.status_code

    else:
        url = _BASE_URL
        url += setting.get(_ONCE) + f"{obj_id}/"

    response = requests.get(url)

    if response.status_code == HTTP_200_OK:
        reg = RegistryRead.model_validate_json(response.content)

        data = RegistryCreateUpdate(
            object_type=reg.object_type,
            name=reg.name,
            object_code=reg.object_code,
            account_id=account_id,
            user_id=user_id,
            project_id=project_id,
            object_item=object_item,
            data=data_to_update.model_dump_json(),
        )

        response = requests.put(url, data=data.model_dump())
        

    return response.status_code


async def delete_by_id(obj_id: UUID, obj_type: RegistryType):
    """Удаление объекта из реестра по идентификатору."""
    setting = REGISTRY_SETTING[obj_type]

    if obj_type in _POLL_SERVICE_TYPE:
        url = _POLL_SERVICE_URL

    else:
        url = _BASE_URL
    url += setting.get(_ONCE) + f"{obj_id}/"

    response = requests.delete(url)
    return response.status_code
