from http import HTTPStatus
import json
from uuid import UUID, uuid4
from fastapi import APIRouter
from fastapi.responses import Response
import requests
from src.config import POLL_SERVICE_URL, USER_SERVICE_URL

from src.result.schemas import ResultRead, ResultCreateUpdate
from src.registry.crud import load_by_id, save_object, load_objects, update_by_id, load_counts
from src.registry.schemas import RegistryType

_POLL_SERVICE_URL = POLL_SERVICE_URL

_USER_SERVICE_URL = USER_SERVICE_URL

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get('/{answer_id}', response_model=ResultCreateUpdate)
async def get_result_by_answer(answer_id: UUID, response: Response):
    """
    **answer_id** - UUID ответов, по которым нужно провести подсчет<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.<br>
    для теста b6f824d4-7374-42ef-9f86-44f6da498d02<br>
    """
    answer, status = await load_by_id(answer_id, RegistryType.answer, method_type="result_by_answer")

    # Load the poll from the database based on its ID.
    poll, status = await load_by_id(answer['pollId'], RegistryType.poll)
    # Convert the poll dictionary into a plain dictionary.
    poll = dict(poll)
    # Extract the poll name from the poll dictionary.
    results = {'pollId': answer['pollId'],
               'pollName': poll['pollName'],
               'templateId': answer['templateId'],
               'userId': answer['userId'],
               'results': {}}

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


@router.get('/{company_id}/{poll_id}/get_analytic_feeling')
async def get_analytic_feeling(company_id: UUID, poll_id: UUID, response: Response):
    """
    **company_id** - UUID компании, по которым нужно провести подсчет<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.
    """
    url = f'{_POLL_SERVICE_URL}answers/company/{company_id}'
    response = requests.get(url)
    answers = json.loads(response.text)

    results = {'companyId': str(company_id),
               'pollId': str(poll_id),
               'results': {}}

    dict_results = results['results']
    for answer in answers:
        if answer['pollId'] == str(poll_id):
            list_answers = answer['answers']

            for answer_ in list_answers:
                answer_value = answer_['answer'][0]
                if answer_['text'] not in dict_results:
                    dict_results[answer_['text']] = int(answer_value['value'])
                else:
                    dict_results[answer_['text']] += int(answer_value['value'])

    return results


@router.get('/{company_id}/{poll_id}/get_analytic_branch')
async def get_analytic_branch(company_id: UUID, poll_id: UUID, response: Response):
    """
    **company_id** - UUID компании, по которым нужно провести подсчет<br>
    Данные берутся из сервиса пользователей, company_id = organization_id<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.<br>
    """
    users_url = f'{_USER_SERVICE_URL}users?organization_id={company_id}'

    answers_url = f'{_POLL_SERVICE_URL}answers/company/{company_id}'

    response = requests.get(users_url)
    users = json.loads(response.text)

    response = requests.get(answers_url)
    answers = json.loads(response.text)

    answer_user_list = []

    for answer in answers:
        if str(answer['pollId']) == str(poll_id):
            if str(answer['pollId']) not in answer_user_list:
                answer_user_list.append(str(answer['userId']))

    results = {'companyId': str(company_id),
               'pollId': str(poll_id),
               'results': {}}

    dict_results = results['results']
    for user in users:
        if user['user_id'] in answer_user_list:
            user_info = user['additional_info']
            city = user_info['city']
            if city:
                if city not in dict_results:
                    dict_results[city] = 1

                else:
                    dict_results[city] += 1

    return results


@router.get('/{company_id}/{poll_id}/get_analytic_position')
async def get_analytic_position(company_id: UUID, poll_id: UUID, response: Response):
    """
    **company_id** - UUID компании, по которым нужно провести подсчет<br>
    Данные берутся из сервиса пользователей, company_id = organization_id
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.<br>
    """
    users_url = f'{_USER_SERVICE_URL}users?organization_id={company_id}'

    answers_url = f'{_POLL_SERVICE_URL}answers/company/{company_id}'

    response = requests.get(users_url)
    users = json.loads(response.text)

    response = requests.get(answers_url)
    answers = json.loads(response.text)

    answer_user_list = []

    for answer in answers:
        if str(answer['pollId']) == str(poll_id):
            if str(answer['pollId']) not in answer_user_list:
                answer_user_list.append(str(answer['userId']))

    results = {'companyId': str(company_id),
               'pollId': str(poll_id),
               'results': {}}

    dict_results = results['results']
    for user in users:
        if user['user_id'] in answer_user_list:
            user_info = user['additional_info']
            position = user_info['position']
            if position:
                if position not in dict_results:
                    dict_results[position] = 1

                else:
                    dict_results[position] += 1

    return results


@router.get('/{company_id}/{poll_id}/get_analytic_gender')
async def get_analytic_gender(company_id: UUID, poll_id: UUID, response: Response):
    """
    **company_id** - UUID компании, по которым нужно провести подсчет<br>
    Данные берутся из сервиса пользователей, company_id = organization_id
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.<br>
    """
    users_url = f'{_USER_SERVICE_URL}users?organization_id={company_id}'

    answers_url = f'{_POLL_SERVICE_URL}answers/company/{company_id}'

    response = requests.get(users_url)
    users = json.loads(response.text)

    response = requests.get(answers_url)
    answers = json.loads(response.text)

    answer_user_list = []

    for answer in answers:
        if str(answer['pollId']) == str(poll_id):
            if str(answer['pollId']) not in answer_user_list:
                answer_user_list.append(str(answer['userId']))

    results = {'companyId': str(company_id),
               'pollId': str(poll_id),
               'results': {}}

    dict_results = results['results']
    for user in users:
        if str(user['user_id']) in answer_user_list:
            user_info = user['additional_info']
            sex = user_info['sex']
            if sex:
                if sex not in dict_results:
                    dict_results[sex] = 1

                else:
                    dict_results[sex] += 1

    return results


@router.get('/{company_id}/{poll_id}/get_analytic_general')
async def get_analytic_general(company_id: UUID, poll_id: UUID, response: Response):
    """
    **company_id** - UUID компании, по которым нужно провести подсчет<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.
    """
    url = f'{_POLL_SERVICE_URL}answers/company/{company_id}'
    response = requests.get(url)
    answers = json.loads(response.text)

    params = [{'normal': [0, 20]}, {'middle': [21, 60]}, {'hard': [61, 120]}]

    results = {'companyId': str(company_id),
               'pollId': str(poll_id),
               'results': {
                   "passed": 0,
                   "feeling": {},
                   "state": {}
    }}

    dict_results = results['results']
    dict_feeling = dict_results['feeling']
    dict_state = dict_results['state']

    for answer in answers:
        if answer['pollId'] == str(poll_id):
            dict_results['passed'] += 1
            count_results = 0
            list_answers = answer['answers']

            for answer_ in list_answers:

                answer_value = answer_['answer'][0]

                count_results += int(answer_value['value'])

                if answer_['text'] not in dict_feeling:
                    dict_feeling[answer_['text']] = int(answer_value['value'])

                else:
                    dict_feeling[answer_['text']] += int(answer_value['value'])

            for values in params:
                key = list(values.keys())[0]
                print(key)
                if key not in dict_state:
                    dict_state[key] = 0

            for values in params:
                value = list(values.values())[0]
                key = list(values.keys())[0]
                if count_results in range(value[0], value[1]+1):
                    dict_state[key] += 1

            

    return results


@router.get('/{company_id}/{poll_id}/get_analytic_branch_state')
async def get_analytic_branch_state(company_id: UUID, poll_id: UUID, response: Response):
    """
    **company_id** - UUID компании, по которым нужно провести подсчет<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.
    """
    url_answers = f'{_POLL_SERVICE_URL}answers/company/{company_id}'
    response = requests.get(url_answers)
    answers = json.loads(response.text)

    url_users = f'{_USER_SERVICE_URL}users?organization_id={company_id}'
    response = requests.get(url_users)
    users = json.loads(response.text)

    params = [{'normal': [0, 20]}, {'middle': [21, 60]}, {'hard': [61, 120]}]

    results = {'companyId': str(company_id),
               'pollId': str(poll_id),
               'results': {}
               }

    dict_results = results['results']

    users_city = {}

    for user in users:
        user_info = user['additional_info']
        city = user_info['city']
        if city:
            user_id = str(user['user_id'])
            if user_id not in users_city:
                users_city[user_id] = city

    for answer in answers:
        if answer['pollId'] == str(poll_id):
            print(answer['userId'])
            if answer['userId'] in users_city:
                user_id = answer['userId']
                user_city = users_city[user_id]
                count_results = 0
                list_answers = answer['answers']
                if user_city not in dict_results:
                    dict_results[user_city] = {}

                city_dict = dict_results[user_city]

                for answer_ in list_answers:
                    answer_value = answer_['answer'][0]
                    count_results += int(answer_value['value'])

                for values in params:
                    key = list(values.keys())[0]
                    if key not in city_dict:
                        city_dict[key] = 0

                for values in params:
                    value = list(values.values())[0]
                    key = list(values.keys())[0]
                    if count_results in range(value[0], value[1]+1):
                        city_dict[key] += 1

            
                    
    return results


@router.get('/{company_id}/{poll_id}/get_analytic_position_state')
async def get_analytic_position_state(company_id: UUID, poll_id: UUID, response: Response):
    """
    **company_id** - UUID компании, по которым нужно провести подсчет<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.
    """
    url_answers = f'{_POLL_SERVICE_URL}answers/company/{company_id}'
    response = requests.get(url_answers)
    answers = json.loads(response.text)

    url_users = f'{_USER_SERVICE_URL}users?organization_id={company_id}'
    response = requests.get(url_users)
    users = json.loads(response.text)

    params = [{'normal': [0, 20]}, {'middle': [21, 60]}, {'hard': [61, 120]}]

    results = {'companyId': str(company_id),
               'pollId': str(poll_id),
               'results': {}
               }

    dict_results = results['results']

    users_position = {}

    for user in users:
        user_info = user['additional_info']
        position = user_info['position']
        if position:
            user_id = str(user['user_id'])
            if user_id not in users_position:
                users_position[user_id] = position

    for answer in answers:
        if answer['pollId'] == str(poll_id):
            print(answer['userId'])
            if answer['userId'] in users_position:
                user_id = answer['userId']
                user_position = users_position[user_id]
                count_results = 0
                list_answers = answer['answers']
                if user_position not in dict_results:
                    dict_results[user_position] = {}

                position_dict = dict_results[user_position]

                for answer_ in list_answers:
                    answer_value = answer_['answer'][0]
                    count_results += int(answer_value['value'])

                for values in params:
                    key = list(values.keys())[0]
                    if key not in position_dict:
                        position_dict[key] = 0

                for values in params:
                    value = list(values.values())[0]
                    key = list(values.keys())[0]
                    if count_results in range(value[0], value[1]+1):
                        position_dict[key] += 1

            
                    
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
