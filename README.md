# Телеграм бот для помощи с выбором курсов V0.4.0
Ссылка на репозиторий в Github: https://github.com/Xiandec/GPB_GPT_Hack

*Бот поддерживает несколько диалогов одновременно*
## Запуск
Для запуска необходимо создать `config.yaml` в корневой папке:
```
bot_token: 1896059860:AAGB9bfnm1HDdQ6S5lMoSPzmEwmDZctYlVE # Токен для телеграм бота
enable_proxy: false # Использовать метод без авторизации при помощи бесплатных прокси true - да, false - нет
API_token_deepinfra: Bearer jwt:aASdsPJKlkjdwlKjs # Если использование прокси отключено вставить апи токен
```
Запукать `main.py`

С параметром `enable_proxy: true` бот может работать долго, 
лучше запускать с `enable_proxy: false` и `API_token_deepinfra`

# Модули
### `helper`
```
helper
├── config.py
└── fp.py
```
Хранятся вспомогательные модули.

Модуль `config.py` отвечает за подгрузку конфигурационных переменных из `.yaml`

Модуль `fp.py` отвечает за поиск всех доступных прокси на данный момент. 
Если в конфиге параметр `enable_proxy` включен (`true`) то бот будет использовать доступные прокси для запросов в *deepinfra*. 
На каждый прокси доступно 5 бесплатных запросов.
### `reference`
```
reference
├── HR.py
├── deepinfra.py
└── main.py
```
Файлы выданные для референса на хакатоне
### `telegram_bot`
```
telegram_bot
└── bot.py
```
Модуль `bot.py` отвечает за основные роутеры и конфигурации для бота телеграм
### `neirwork`
```
neirwork
├── controller.py
├── data
│   ├── course.json
│   └── system_conf.py
└── proxy_controller.py
```
Модуль отвечает за работу с нейронной сетью.

 - `DeepinfraController` - отвечает за создание и хранение контекста, создание запроса для API
   - `_set_assumption` - установить предположительный курс
   - `get_assumption` - получить курс, который больше всего подходит
   - `_get_system_info` - при инициализации класса задаётся основной контекст бота
   - `_create_headers` - создаёт заголовки для запроса с авторизацией
   - `_decode_response` - декодирует ответ нейронной сети
   - `create_json_data` - возвращает JSON данные для запроса
   - `add_message` - добавляет сообщение в контекст
   - `clear_messages` - очищает контекст
   - `get_messages` - получить все сообщения из диалога


 - `AvalibleProxies` - отвечает за хранение и создание словарей для запроса для API
   - `update_proxies` - обновляет список доступных прокси
   - `get_available_proxies` - получить доступные прокси на данный момент
   - `update_used_proxies` - добавление прокси в список использованных
   - `ip_to_proxy` - преобразует `IP` в словарь для `requests`

## CHANGELOG

---

## V0.4.0 - 17:05 12.04.24
Добавлена поддержка нескольких диалогов одновременно

## V0.3.0 - 01:45 11.04.24
Изменён промт, добавленно ограничение по сообщениям и добавлен хендлер канала для автоматического тестирования

## V0.2.1 - 22:15 10.04.24
Изменён промт и добавлены методы для контроллера нейронной сети

## V0.2.0 - 23:35 9.04.24
Изменена логика запроса и добавлена авторизация по `api key` на *deepinfra*

## V0.1.0 - 05:00 9.04.24
Телеграм бот работает и отвечает на сообщения

## V0.0.0 - 02:00 9.04.24
Основная структура бота
