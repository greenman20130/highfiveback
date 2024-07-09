from http import HTTPStatus
import json
from uuid import UUID, uuid4
from fastapi import APIRouter
from fastapi.responses import Response
import requests
from src.config import POLL_SERVICE_URL, USER_SERVICE_URL

from src.result.schemas import ResultRead, ResultCreateUpdate

from src.registry.schemas import RegistryType

_POLL_SERVICE_URL = POLL_SERVICE_URL

_USER_SERVICE_URL = USER_SERVICE_URL

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get('/{answer_id}')
async def get_result_by_answer(answer_id: UUID, response: Response):
    """
    **answer_id** - UUID ответов, по которым нужно провести подсчет<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.<br>
    для теста 731b154e-c3dd-4e62-9c77-b90764e51e9e<br>
    """
    url = f'{_POLL_SERVICE_URL}answers/{answer_id}'
    response = requests.get(url)
    answer = json.loads(response.text)

    url = f'{_POLL_SERVICE_URL}polls/{answer["pollId"]}'
    response = requests.get(url)
    poll = json.loads(response.text) 

    poll = dict(poll)

    results = {'pollId': answer['pollId'],
               'pollName': poll['pollName'],
               'templateId': answer['templateId'],
               'userId': answer['userId'],
               'points': {}}
    
    dict_results = results['points']
    list_answers = answer['answers']
    for answer_ in list_answers:
        answer_value = answer_['answer'][0]
        if answer_['text'] not in dict_results:
            dict_results[answer_['text']] = int(answer_value['value'])
        else:
            dict_results[answer_['text']] += int(answer_value['value'])
    
    url = f'{_POLL_SERVICE_URL}templates/{answer["templateId"]}'
    response = requests.get(url)
    template_key = json.loads(response.text)
    template_key = json.loads(template_key['templateDescription'].replace("'",'"'))
    detail_key = template_key['detailResult']
    global_key = template_key['globalResult']
    result_for_global = {}

    for r_key, r_value in dict_results.items():
        detail_key_cycle = detail_key[r_key]
        for t_key, t_value in detail_key_cycle.items():
            if r_value in range(t_value[0], t_value[1]+1):
                dict_results[r_key] = int(t_key)
    
    global_result = 0

    for rg_key, rg_value in dict_results.items():
        global_result += rg_value
    for g_key, g_value in global_key.items():
        if global_result in range(g_value[0], g_value[1]+1):
            results['result'] = g_key   

    return results

@router.get('/{poll_id}/poll_statistics')
async def get_poll_statistics(poll_id: UUID, response: Response):
    """
    **poll_id** - UUID опроса, по которой нужно провести подсчет<br>
    **return** Список опросов, HTTP_200_OK. При неудаче - статус ошибки.
    """
    url = f'{_POLL_SERVICE_URL}polls/{poll_id}'
    response = requests.get(url)
    poll = json.loads(response.text)
    result = {'pollId': poll_id,
              'sex':{'male': 0, 'female': 0},
              'city':{},
              'positions':{},
              'points':{},
              'states':{},
              }
    city = result['city']
    positions = result['positions']
    states = result['states']
    sex = result['sex']
    points = result['points']   
    users = poll['questions']
    for user in users:
        options = user['options']
        user_info = options[0]
        user_info = user_info['value']
        user_info = user_info.replace("true", 'True')
        user_info = eval(user_info)
        additional_info = user_info['additional_info']
        point = eval(user['description'])
        city_info = additional_info['city']
        states_info = user['text']
        if user['text'] not in states:
            states[states_info] = 1

        else:
            states[states_info] += 1

        if additional_info['city'] not in city:
            city[city_info] = {}
            ct = city[city_info]
            ct[states_info] = 1
            
        else:
            ct = city[city_info]
            if states_info not in ct:
                ct[states_info] = 1
            else:
                ct[states_info] += 1

        sex_info = additional_info['sex']
        sex[sex_info] += 1
        position_info = additional_info['position']
        if position_info not in positions:
            positions[position_info] = {}
            pos = positions[position_info]
            pos[states_info] = 1

        else:
            pos = positions[position_info]
            if states_info not in pos:
                pos[states_info] = 1
            else:
                pos[states_info] += 1

        for key, value in point.items():
            if key not in points:
                points[key] = value
            else:
                points[key] += value

    return result
