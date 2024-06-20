"""
Сервисные установки для автоматизации чтения/записи данных в реестры
"""
from src.chat.schemas import ChatUsers
from src.registry.schemas import RegistryType


_ONCE = 1
_MANY = 2
_STRUCT = 3

# словарь подстановок для унификации работы реестров
REGISTRY_SETTING = {
    RegistryType.chat: {_ONCE: "chat/", _MANY: "chats/", _STRUCT: ChatUsers},
}
