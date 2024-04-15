import requests
from helper.config import Config
from neirwork.data.system_conf import SYS_MSG
import json
import re

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

class DeepinfraController():
    """
    Контроллер для работы с API Deepinfra
    """
    def __init__(self) -> None:
        self._model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
        self._messages = []
        self._stream = True
        self._assumption = '[Машинное обучение]'
        self._state = 0
        self._max_stages = 4
        self._get_system_info()

    def _set_assumption(self, value: str) -> None:
        self._assumption = value

    def get_assumption(self) -> str:
        return self._assumption

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
        with open('neirwork/data/course.json') as f:
            courses = json.loads(f.read())
        
        if USE_PROXY:
            pr = AvalibleProxies()
            proxies = pr.get_available_proxies()
    
            proxies = pr.ip_to_proxy(proxies[0])
            try:
                response = requests.post('https://api.deepinfra.com/v1/openai/chat/completions', json=self._create_json_data(), proxies=proxies)
            except BaseException:
                pr.update_used_proxies(proxies['https'])
            if response.status_code == 200: # Если ответ есть
                resp_text = self._decode_response(response.text)
                if resp_text:

                    #if len(re.findall('\\[.*\\]', resp_text)) > 0: # Добавить курс, если он существует
                    #    self._set_assumption(re.findall('\\[.*\\]', resp_text)[0])
                    
                    list_assumption = [i for i in [course['Course_name'] for course in courses] if i in resp_text] # Поиск курса в ответе
                    if len(list_assumption) > 0:  # Добавить курс, если он существует
                        list_assumption = sorted(list_assumption, key=len, reverse=True)
                        self._set_assumption('[' + list_assumption[0] + ']')

                    self.add_message(resp_text, 'assistant')

                    self._state += 1
                    if self._state >= self._max_stages: # Вернуть курс, если достигнут лимит сообщений
                        return self.get_assumption()
                    
                    return resp_text
            else:
                pr.update_used_proxies(proxies['https'])
                return None
        else:
            API_KEY = conf.get_value('API_token_deepinfra')
            headers = self._create_headers(API_KEY)
            json_data = self._create_json_data()
            response = requests.post('https://api.deepinfra.com/v1/openai/chat/completions', headers=headers, json=json_data)
            if response.status_code == 200: # Если ответ есть
                try:
                    resp_text = self._decode_response(response.text.strip())
                except BaseException:
                    return None
                if resp_text:

                    #if len(re.findall('\\[.*\\]', resp_text)) > 0: # Добавить курс, если он существует
                    #    self._set_assumption(re.findall('\\[.*\\]', resp_text)[0])
                    
                    list_assumption = [i for i in [course['Course_name'] for course in courses] if i in resp_text] # Поиск курса в ответе
                    if len(list_assumption) > 0:  # Добавить курс, если он существует
                        list_assumption = sorted(list_assumption, key=len, reverse=True)
                        self._set_assumption('[' + list_assumption[0] + ']')

                    self.add_message(resp_text, 'assistant')

                    self._state += 1
                    if self._state >= self._max_stages: # Вернуть курс, если достигнут лимит сообщений
                        return self.get_assumption()
                    
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
        self._assumption = '[Машинное обучение]'
        self._state = 0
        self._get_system_info()

    def get_messages(self, ) -> str:
        """
        Возвращает контекст
        """
        return '\n\n'.join([i['content'] for i in self._messages if i['role'] != 'system'])
