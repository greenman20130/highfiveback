import logging
import os.path
from typing import Any
from dotenv import load_dotenv, find_dotenv


class EndpointFilter(logging.Filter):
    def __init__(self, path: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._path = path

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find(self._path) == -1


logging.basicConfig(
    level=logging.INFO, filename="info.log", format="[%(asctime)s - %(levelname)s - %(pathname)s]: %(message)s"
)
logger = logging.getLogger()

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(EndpointFilter(path="/ping"))

_LOCAL_HOSTS = 'http://localhost;https://localhost;http://127.0.0.1;https://127.0.0.1'

load_dotenv()


TMP_DIR = os.environ.get('TMP_DIR', '/tmp')
BASE_REGISTRY_URL = os.environ.get('BASE_REGISTRY_URL', 'http://127.0.0.1:8001/api/')
POLL_SERVICE_URL = os.environ.get('POLL_SERVICE_URL', 'https://api.opros.skroy.ru/')
USER_SERVICE_URL = os.environ.get('POLL_SERVICE_URL', 'https://api.users.skroy.ru/')
ALLOWED_ORIGINS = _LOCAL_HOSTS
origins = os.environ.get("ALLOWED_ORIGINS")
if origins is not None:
    ALLOWED_ORIGINS += f';{origins}'
