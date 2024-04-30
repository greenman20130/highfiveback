import csv
import json
import tempfile
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter
from http import HTTPStatus

from src.registry.schemas import RegistryType
from src.registry.crud import save_object, load_objects, load_by_id
from src.answer.schemas import *
from src.config import TMP_DIR
from fastapi.responses import FileResponse, Response

router = APIRouter(prefix="/answers", tags=["Answer"])


@router.post('')
async def post_answers(answers: QuestResult, response: Response):
    """
    Сохранение ответов респондента.<br>
    **answers** - данные для сохранения<br>
    **return** - статусы операции:<br>
        **_HTTP_201_CREATED_** - данные сохранены<br>
        **_HTTP_409_CONFLICT_** - попытка сохранить данные при неактивном опросе
    """
    id = {"id": None}
    date_now = datetime.now(timezone.utc)

    poll, status = await load_by_id(answers.pollId, RegistryType.poll)
    print('ok')

    if status == HTTPStatus.OK:
        print('2')
        if poll.dateStart is None or not poll.active:
            print('---')
            status = HTTPStatus.CONFLICT
        elif poll.dateEnd is None:
            print('3')
            if poll.dateStart <= date_now:
                print('4')
                id, status = await save_object(answers, RegistryType.answer,
                                               object_item=answers.pollId,
                                               account_id=poll.companyId)
            else:
                status = HTTPStatus.CONFLICT
                print('ok')
        elif poll.dateStart <= date_now <= poll.dateEnd:
            id, status = await save_object(answers, RegistryType.answer,
                                           object_item=answers.pollId,
                                           account_id=poll.companyId)
        else:
            status = HTTPStatus.CONFLICT
    response.status_code = status
    return id


# Only For Test
# @router.get("all")
# async def get_all(poll_id: UUID, response: Response):
#     quests_result, status = await load_objects(RegistryType.answer, f"?object_item={poll_id}")
#     response.status_code = status
#     return quests_result

#FIX LATER
# @router.get('/{poll_id}/company/{company_id}/csv')
# async def get_answers_csv(poll_id: UUID, company_id: UUID, response: Response):
#     """
#     Получение результатов опроса в виде файла **_data.csv_**.<br>
#     **poll_id** Идентификатор опроса, по которому необходимы результаты<br>
#     **company_id** Идентификатор компании<br>
#     **return** Статусы операции:<br>
#         **_HTML_200_OK_** - файл сформирован<br>
#         **_HTTP_422_UNPROCESSABLE_ENTITY_** - ошибка валидации полученных данных по заданному опросу<br>
#         **_HTTP_404_NOT_FOUND_** - данные для выгрузки не найдены
#     """
#     quests_result, status = await load_objects(RegistryType.answer, f"?object_item={poll_id}&account_id={company_id}")
#     response.status_code = status

#     if status == HTTPStatus.OK:
#         answers = []
#         fields_names = []

#         for q in quests_result:
#             answer_row = {
#                 'Дата ответа': datetime.fromisoformat(q['created_date']).strftime('%d.%m.%Y %H:%M'),
#                 'Номер ответа': f'{q["id"]}',
#             }
#             for a in q['answers']:
#                 if len(a["answer"]) > 1:
#                     answer_row[f'{a["text"]}'] = (':'.join([f"{v['value']}" for v in a["answer"]])
#                                                   .replace(';', ',').replace('\n', ' '))
#                 else:
#                     answer_row[f'{a["text"]}'] = a["answer"][0]['value'].replace(';', ',').replace('\n', ' ')

#             fields_names.extend([f for f in answer_row.keys() if f not in fields_names])
#             answers.append(answer_row)

#         with tempfile.NamedTemporaryFile(dir=TMP_DIR, mode="wt", suffix='.csv', newline="",
#                                          delete=False, encoding='utf-8-sig') as tmp_file:

#             writer = csv.DictWriter(tmp_file, fieldnames=fields_names, dialect='excel',
#                                     quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
#             writer.writeheader()
#             writer.writerows(a for a in answers)

#         return FileResponse(path=tmp_file.name, filename='data.csv', media_type='application/csv')

#FIX LATER
# @router.get('/{poll_id}/company/{company_id}/json')
# async def get_answers_json(poll_id: UUID, company_id: UUID, response: Response):
#     """
#     Получение результатов опроса в виде файла **_data.json_**.<br>
#     **poll_id** Идентификатор опроса, по которому необходимы результаты<br>
#     **company_id** Идентификатор компании<br>
#     **return** Статусы операции:<br>
#         **_HTML_200_OK_** - файл сформирован<br>
#         **_HTTP_422_UNPROCESSABLE_ENTITY_** - ошибка валидации полученных данных по заданному опросу<br>
#         **_HTTP_404_NOT_FOUND_** - данные для выгрузки не найдены
#     """
#     answer, status = await load_by_id(poll_id, RegistryType.answer, method_type="answers_json", second_id=company_id)
#     response.status_code = status
#     print('ok')

#     if status == HTTPStatus.OK:
#         result = {"pollId": f"{poll_id}"}
#         answers = []

#         for q in answer:
#             answers.append({'answers': q['answers']})
#         print('ЕБАШУ')
#         result['result'] = answers
#         with tempfile.NamedTemporaryFile(dir=TMP_DIR, mode="wt", suffix='.json', newline="",
#                                          delete=False, encoding='utf-8') as tmp_file:
#             json.dump(result, tmp_file, indent=5)

#         return FileResponse(path=tmp_file.name, filename='data.json', media_type='application/json')

#     return


@router.get('/{answer_id}', response_model=QuestResultRead)
async def get_answer_by_id(answer_id: UUID, response: Response):
    answer, status = await load_by_id(answer_id, RegistryType.answer)
    response.status_code = status
    return answer


@router.get('/company/{company_id}')
async def get_answers_by_company_id(company_id: UUID, response: Response):
    quests_result, status = await load_objects(RegistryType.answer, f"?account_id={company_id}")
    if status == HTTPStatus.OK:
        return quests_result

