"""
Сервисные установки для автоматизации чтения/записи данных в реестры
"""
from src.answer.schemas import QuestResultRead
from src.poll.schemas import PollRead
from src.registry.schemas import RegistryType
from src.template.schemas import TemplateRead
from src.user.schemas import UserRead
from src.company.schemas import CompanyRead
from src.chat.schemas import ChatRead
from src.result.schemas import ResultRead


_ONCE = 1
_MANY = 2
_STRUCT = 3

# словарь подстановок для унификации работы реестров
REGISTRY_SETTING = {
    RegistryType.template: {_ONCE: "template/", _MANY: "templates/", _STRUCT: TemplateRead},
    RegistryType.poll: {_ONCE: "poll/", _MANY: "polls/", _STRUCT: PollRead},
    RegistryType.answer: {_ONCE: "answer/", _MANY: "answers/", _STRUCT: QuestResultRead},
    RegistryType.user: {_ONCE: "user/", _MANY: "users/", _STRUCT: UserRead},
    RegistryType.company: {_ONCE: "company/", _MANY: "companies/", _STRUCT: CompanyRead},
    RegistryType.chat: {_ONCE: "chat/", _MANY: "chats/", _STRUCT: ChatRead},
    RegistryType.result: {_ONCE: "result/", _MANY: "results/", _STRUCT: ResultRead},
}
