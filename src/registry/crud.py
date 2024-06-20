"""
Работа с реестрами
"""
import json
from uuid import UUID, uuid4
from typing import Any

from src.config import BASE_REGISTRY_URL
from src.registry.schemas import RegistryType, RegistryCreateUpdate, RegistryRead, RegistryMultiple
from src.registry.service_data import REGISTRY_SETTING, _MANY, _STRUCT, _ONCE

from pydantic import ValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK, HTTP_201_CREATED
import requests

_BASE_URL = f"{BASE_REGISTRY_URL}"


async def load_objects(obj_type: RegistryType, filter_options: str = None) -> (
        tuple[None, Any] | tuple[str, int] | tuple[None, int]):
    """Чтение списка объектов из реестра

    Returns:
        object: 
    """
    setting = REGISTRY_SETTING.get(obj_type)
    url = _BASE_URL + setting[_MANY]

    if filter_options is not None:
        url += filter_options
    response = requests.get(url)

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
    url = _BASE_URL + setting[_MANY]

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


async def load_by_id(obj_id: UUID, obj_type: RegistryType):
    """
    Чтение объекта из реестра
    """
    setting = REGISTRY_SETTING.get(obj_type)
    url = _BASE_URL + setting[_ONCE] + f"{obj_id}/"
    response = requests.get(url)

    if response.status_code == HTTP_200_OK:
        try:
            reg = RegistryRead.model_validate_json(response.content)
            obj = setting[_STRUCT].model_validate(reg.data)
            if hasattr(obj, 'created_date'):
                obj.created_date = reg.modified_date

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
    url = _BASE_URL + setting[_ONCE]

    uuid_reg = uuid4()
    id = None
       
    data = RegistryCreateUpdate(
        id=uuid_reg,
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
    url = _BASE_URL + setting.get(_ONCE) + f"{obj_id}/"

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

    return response.status_code


async def delete_by_id(obj_id: UUID, obj_type: RegistryType):
    """Удаление объекта из реестра по идентификатору."""
    setting = REGISTRY_SETTING[obj_type]
    url = _BASE_URL + setting.get(_ONCE) + f"{obj_id}/"

    response = requests.delete(url)
    return response.status_code
