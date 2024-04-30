import json
from uuid import UUID

from fastapi import APIRouter, Response, UploadFile

from src.registry.crud import save_object, load_objects, load_by_id, update_by_id
from src.registry.schemas import RegistryType
from src.template.schemas import TemplateObject, TemplateRead
from starlette.status import HTTP_200_OK, HTTP_406_NOT_ACCEPTABLE

router = APIRouter(prefix="/templates", tags=["Template"])


@router.get('/', response_model=list[TemplateRead])
async def get_templates_list(response: Response, account_id: UUID = None):
    templates, status = await load_objects(RegistryType.template)

    if account_id is None:
        tmp_list = [t for t in templates if t['companyId'] is not None]
    else:
        tmp_list = [t for t in templates if t['companyId'] is not None and t['companyId'] != str(account_id)]

    for t in tmp_list:
        templates.remove(t)

    response.status_code = status
    return templates


@router.get('/{template_id}', response_model=TemplateRead)
async def get_template_by_id(template_id: UUID, response: Response):
    template, status = await load_by_id(template_id, RegistryType.template)
    response.status_code = status
    return template


@router.post('/')
async def post_template(template: TemplateRead, response: Response):
    data_to_save = TemplateRead(**template.model_dump())

    content, status = await save_object(data_to_save, RegistryType.template,
                                        user_id=template.userId,
                                        account_id=template.accountId)
    response.status_code = status
    return content


@router.put('/')
async def put_template(template_id: UUID, template: TemplateRead, response: Response):
    templ_update = TemplateRead(**template.model_dump())
    status = await update_by_id(template_id, templ_update, RegistryType.template,
                                account_id=template.accountId,
                                user_id=template.userId)
    response.status_code = status
    return


@router.post('/upload')
async def upload_templates(file_template: UploadFile, response: Response):
    response.status_code = HTTP_200_OK
    try:
        template_list = json.load(file_template.file)
        for template in template_list:
            if not hasattr(template, 'accountId'):
                template['accountId'] = None
            if not hasattr(template, 'userId'):
                template['userId'] = None

            await save_object(TemplateObject.model_validate(template), RegistryType.template,
                              account_id=template['accountId'],
                              user_id=template['userId'])
    except:
        response.status_code = HTTP_406_NOT_ACCEPTABLE
    return

# @router.post('/user_post')
# async def user_post(template: TemplateObject, response: Response):
#     content, status = await save_object(template, RegistryType.template)
#     response.status_code = status
#     return content
