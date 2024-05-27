import json

import requests
from uuid import uuid4
from src.answer.schemas import QuestResult

from src.config import BASE_REGISTRY_URL
from fastapi.responses import Response


class AnswerService:
    @staticmethod
    async def post_answer_in_registry(result: QuestResult):
        """
        Добавление ответов в реестр
        """

        object_id = uuid4()
        answer_data = {
            "object_type": "answer",
            "name": f"answer_{object_id}",
            "object_code": f"{object_id}",
            "data": result.model_dump_json(),
            "object_item": f'{result.pollId}',
        }

        response = requests.post(f"{BASE_REGISTRY_URL}answer/", json=answer_data)
        answer_id = response.json().get('id')

        return Response(answer_id, status_code=response.status_code)
