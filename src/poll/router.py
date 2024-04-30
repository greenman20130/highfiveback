from http import HTTPStatus
from uuid import UUID
from fastapi import APIRouter
from fastapi.responses import Response

from src.poll.schemas import PollRead, PollCreateUpdate, PollByUserId
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType

router = APIRouter(prefix="/polls", tags=["Poll"])


@router.put("/{poll_id}")
async def put_poll_answers(poll_id: UUID, poll: PollRead, response: Response):
    """
    Изменение опроса в реестре.<br>
    **poll_id** идентификатор опроса<br>
    **poll** данные измененного опроса<br>
    **returns** статусы операции:<br>
    HTTP_200_OK данные изменены
    Пример:
    {
    "userId": "e937332f-34f2-41f1-868a-1eaa8db789e0",
    "editorId": "a39ef778-939c-4349-8734-024d971c99da",
    "companyId": "bd743040-d003-4579-8a34-1da34db38db9",
    "templateId": "e9834cd5-cb33-4b91-b961-6cba2ae04406",
    "adminHeading": "string", хуй знает что это
    "adminDescription": "string", и это
    "pollName": "Водопьянова",
    "pollDescription": "тест водопьяновой",
    "finalHeading": "string", и это
    "finalDescription": "string", и это
    "themeColor": "black",
    "dateStart": "2024-04-29T04:04:23.894Z", дата нача обязательно должна быть меньше текущей
    "dateEnd": "2024-04-29T04:04:23.894Z", позже текущей иначе нельзя залить ответы
    "active": true, обязательно true если нужно залить ответ
    "questions": [ шаблон опроса, он вроде как не сейвится, даже не пытайся, просто вставь то что у меня
        {
        "id": 0,
        "text": "string",
        "description": "string",
        "type": "string",
        "required": true,
        "options": [
            {
            "id": "string",
            "value": "string"
            }
        ]
        }
    ]
    }
    """
    poll.editorId = poll.userId
    old_poll, status = await load_by_id(poll_id, RegistryType.poll)

    
    if status == HTTPStatus.OK:
        poll.userId = old_poll.userId
        if poll.companyId != None:
            account_id = poll.companyId
        else:
            account_id = None
        status = await update_by_id(poll_id, poll, RegistryType.poll,
                                    object_item=poll.templateId,
                                    user_id=old_poll.userId,
                                    account_id=account_id)
    response.status_code = status
    return


@router.get("/{poll_id}", response_model=PollRead)
async def get_poll_for_answers(poll_id: UUID, response: Response):
    """
    Выдача опроса для ответа респондентом.<br>
    **poll_id** Идентификатор опроса<br>
    **return** Опрос PollRead + статус **__HTTP_200_OK__**. Если опрос не найден - статус **__HTTP_404_NOT_FOUND__**.
    """
    poll, status = await load_by_id(poll_id, RegistryType.poll)
    # сбросить Id компании
    # poll.companyId = None
    
    response.status_code = status

    return poll


@router.get("/{company_id}/company", response_model=list[PollByUserId])
async def get_polls_by_company(company_id: UUID, response: Response):
    """Список опросов компании<br>
    **company_id** - UUID компании, по которой выбирается список опросов<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.
    """
    result, status = await load_by_id(company_id, RegistryType.poll, method_type='polls_by_company')

    response.status_code = status
    return result


@router.get("/{user_id}/user", response_model=list[PollByUserId])
async def get_polls_by_user(user_id: UUID, response: Response):
    """Список всех опросов пользователя<br>
    **user_id** Идентификатор пользователя<br>
    **return** Список опросов, HTTP_200_OK.
    """
    result, status = await load_by_id(user_id, RegistryType.poll, method_type='polls_by_user')

    response.status_code = status
    return result


@router.get("/{template_id}/template", response_model=list[PollRead])
async def get_polls_by_template(template_id: UUID, response: Response):
    """Список всех опросов шаблона<br>
    **template_id** Идентификатор шаблона<br>
    **return** Список опросов, HTTP_200_OK.
    """

    result, status = await load_by_id(template_id, RegistryType.poll, method_type='polls_by_template')

    response.status_code = status
    return result


@router.post("")
async def post_poll(poll: PollCreateUpdate, response: Response):
    """
    Передача опроса для сохранения в реестры<br>
    **return** Структура опроса в виде JSON + статус 200.

    HTTP_200_OK данные изменены
    Пример:
    {
    "userId": "e937332f-34f2-41f1-868a-1eaa8db789e0",
    "editorId": "a39ef778-939c-4349-8734-024d971c99da",
    "companyId": "bd743040-d003-4579-8a34-1da34db38db9",
    "templateId": "e9834cd5-cb33-4b91-b961-6cba2ae04406",
    "adminHeading": "string", хуй знает что это
    "adminDescription": "string", и это
    "pollName": "Водопьянова",
    "pollDescription": "тест водопьяновой",
    "finalHeading": "string", и это
    "finalDescription": "string", и это
    "themeColor": "black",
    "dateStart": "2024-04-29T04:04:23.894Z", дата нача обязательно должна быть меньше текущей
    "dateEnd": "2024-04-29T04:04:23.894Z", позже текущей иначе нельзя залить ответы
    "active": true, обязательно true если нужно залить ответ
    "questions": [ шаблон опроса, он вроде как не сейвится, даже не пытайся, просто вставь то что у меня
        {
        "id": 0,
        "text": "string",
        "description": "string",
        "type": "string",
        "required": true,
        "options": [
            {
            "id": "string",
            "value": "string"
            }
        ]
        }
    ]
    }
    """
    user_id = poll.userId
    account_id = poll.companyId
    template_id = poll.templateId

    id, status = await save_object(poll, RegistryType.poll,
                                   user_id=user_id, account_id=account_id, object_item=template_id)
    response.status_code = status
    return id
