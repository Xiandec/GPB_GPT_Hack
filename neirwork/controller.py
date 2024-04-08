import requests
from helper.config import Config
from neirwork.data.system_conf import SYS_MSG

class DeepinfraController():
    """
    Контроллер для работы с API Deepinfra
    """
    def __init__(self) -> None:
        self._model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
        self._messages = []
        self._stream = True
        self._get_system_info()

    def _get_system_info(self, ) -> dict:
        """
        Задаёт контекст для нейронной сети
        """
        self._messages.append({
            'role': 'system',
            'content': SYS_MSG
            })
        

    def create_json_data(self, ) -> dict:
        """
        Создаёт JSON-данные для запроса
        """
        request = dict()
        request['model'] = self._model
        request['messages'] = self._messages
        request['stream'] = self._stream
        return request
    
    def add_message(
            self, 
            message: str = None, 
            role: str = None
            ) -> None:
        """
        Добавляет сообщение `message` в контекст `role`

        Роли:
         - `system` - системный
         - `user` - пользователь
         - `assistant` - бот
        """
        if message and role:
            message_dict = {
                'role': role,
                'content': message
            }
            self._messages.append(message_dict)
        return
            
