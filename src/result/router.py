from http import HTTPStatus
from uuid import UUID, uuid4
from fastapi import APIRouter
from fastapi.responses import Response

from src.result.schemas import ResultRead, ResultCreateUpdate
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType

router = APIRouter(prefix="/result", tags=["Result"])

@router.get('/{answer_id}', response_model=ResultCreateUpdate)
async def get_result_by_answer(answer_id: UUID, response: Response):
    """
    **answer_id** - UUID ответов, по которым нужно провести подсчет<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.
    для теста b6f824d4-7374-42ef-9f86-44f6da498d02
    """
    answer, status = await load_by_id(answer_id, RegistryType.answer, method_type="result_by_answer")
    

    # Load the poll from the database based on its ID.
    poll, status = await load_by_id(answer['pollId'], RegistryType.poll)
    # Convert the poll dictionary into a plain dictionary.
    poll = dict(poll)
    # Extract the poll name from the poll dictionary.
    results = {'pollId':answer['pollId'],
               'pollName':poll['pollName'],
               'templateId':answer['templateId'],
               'userId':answer['userId'],
               'results':{}}

    dict_results = results['results']
    list_answers = answer['answers']

    for answer_ in list_answers:
        answer_value = answer_['answer'][0]
        if answer_['text'] not in dict_results:
            dict_results[answer_['text']] = int(answer_value['value'])
        else:
            dict_results[answer_['text']] += int(answer_value['value'])

    response.status_code = status
    return results






# @router.post("")
# async def post_result(result: ResultCreateUpdate, response: Response):
#     if result.userId is None:
#         result.userId = uuid4()
    
#     if result.companyId is None:
#         result.companyId = uuid4()
    
#     account_id = result.companyId
#     user_id = result.userId

#     id, status = await save_object(result, RegistryType.result,
#                                    user_id=user_id, account_id=account_id)
#     response.status_code = status
#     return id


# @router.get("/{poll_id}/company/{company_id}/json", response_model=ResultRead)
# async def get_result(poll_id: UUID, company_id: UUID, response: Response):
#     request = request.get(_SERVICE_URL + f'answer/{poll_id}/company/{company_id}/json')
    

    
#     return request


