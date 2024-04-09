import requests
from helper.config import Config
from neirwork.data.system_conf import SYS_MSG
import json

from neirwork.proxy_controller import AvalibleProxies

class Singleton(object):
    """
    Singleton class
    """
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class DeepinfraController(Singleton):
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
    
    def get_responce(self, **kwargs) -> str:
        """
        Возвращает ответ от нейронной сети
        """
        if 'proxies' in kwargs.keys() and kwargs['proxies']:
            pr = AvalibleProxies()
            proxies = pr.get_available_proxies()
    
            proxies = pr.ip_to_proxy(proxies[0])
            response = requests.post('https://api.deepinfra.com/v1/openai/chat/completions', json=self.create_json_data(), proxies=proxies)
            try:
                resp_text = ''.join([json.loads(i)['choices'][0]['delta']['content'] for i in response.text.split('data: ') if i != '' and not '[DONE]' in i and 'content' in json.loads(i)['choices'][0]['delta'].keys()])
                self.add_message(resp_text, 'assistant')
                return resp_text
            except BaseException:
                pr.update_used_proxies(proxies)
                return 'Ошибка'

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
    
    def clear_messages(self, ) -> None:
        """
        Очищает контекст
        """
        self._model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
        self._messages = []
        self._stream = True
        self._get_system_info()