import json
import os.path
from uuid import UUID

from src.registry.crud import save_object, load_objects
from src.registry.schemas import RegistryType
from src.template.schemas import TemplateObject

_TEMPLATES_FILE = os.path.join(os.curdir, 'first_init', 'templates.json')


async def init():
    if os.path.exists(_TEMPLATES_FILE):
        with open(_TEMPLATES_FILE, encoding='utf-8') as f:
            template_list = json.load(f)

        # templates, status = await load_objects(RegistryType.template, "?limit=1")
        # print(templates)

        for template in template_list:
            await save_object(TemplateObject.model_validate(template), RegistryType.template)

        os.remove(_TEMPLATES_FILE)

# response = crud.save_object()
