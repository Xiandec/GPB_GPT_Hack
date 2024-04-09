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
        

    def _create_json_data(self, ) -> dict:
        """
        Создаёт JSON-данные для запроса
        """
        request = dict()
        request['model'] = self._model
        request['messages'] = self._messages
        request['stream'] = self._stream
        return request
    
    def _create_headers(self, api_key) -> dict:
        """
        Создаёт заголовки для запроса с авторизацией
        """
        return {
            'Authorization': api_key,
        }
    
    def _decode_response(
            self,
            response: str = None,
    ) -> str:
        if response and '[DONE]' in response:
            return ''.join([json.loads(i)['choices'][0]['delta']['content'] for i in response.split('data: ') if i != '' and not '[DONE]' in i and 'content' in json.loads(i)['choices'][0]['delta'].keys()])
        return 
    
    def get_responce(self, ) -> str:
        """
        Возвращает ответ от нейронной сети
        """
        conf = Config()
        USE_PROXY = conf.get_value('enable_proxy')
        
        if USE_PROXY:
            pr = AvalibleProxies()
            proxies = pr.get_available_proxies()
    
            proxies = pr.ip_to_proxy(proxies[0])
            response = requests.post('https://api.deepinfra.com/v1/openai/chat/completions', json=self._create_json_data(), proxies=proxies)
            if response.status_code == 200:
                resp_text = self._decode_response(response.text)
                if resp_text:
                    self.add_message(resp_text, 'assistant')
                    return resp_text
            else:
                pr.update_used_proxies(proxies)
                return None
        else:
            API_KEY = conf.get_value('API_token_deepinfra')
            headers = self._create_headers(API_KEY)
            json_data = self._create_json_data()
            response = requests.post('https://api.deepinfra.com/v1/openai/chat/completions', headers=headers, json=json_data)
            if response.status_code == 200:
                resp_text = self._decode_response(response.text)
                if resp_text:
                    self.add_message(resp_text, 'assistant')
                    return resp_text
            else:
                return None


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