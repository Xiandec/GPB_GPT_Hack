# Телеграм бот для помощи с выбором курсов V0.4.3
Ссылка на репозиторий в Github: https://github.com/Xiandec/GPB_GPT_Hack

## Описание
Бот подбирает подходящий курс для пользователя, исходя из его интересов и знаний.

Бот может поддерживать сразу несколько диалогов одновременно при помощи машины состояний. 
Он может отвечать в личных сообщениях пользователю и в канале для автоматического тестирования. 
После запуска бот ждёт сообщение от пользователя и отвечает на него. 
 - `/start` очищает контекст беседы.
 - В личных сообщениях бот заканчивает диалог после того, как отправляет курс в формате `[название_курса]`, после этого контекст беседы автоматически очищается.
После окончания диалога в личных сообщениях не обязательно писать `/start`, бот уже готов обрабатывать новые сообщения в новом контексте.
 - В канале бот заканчивает диалог после того, как отправляет курс в формате `[название_курса]` или бот для тестирования пишет `"Диалог окончен, accuracy = ..."`, после этого контекст беседы автоматически очищается.

Количество сообщений ограниченно на 4х, благодаря этому нейронная сеть не теряет контекст беседы и не начинает переучиваться на сообщениях пользователя. 

## Запуск
Для запуска необходимо создать `config.yaml` в корневой папке:
```
bot_token: 1896059860:AAGB9bfnm1HDdQ6S5lMoSPzmEwmDZctYlVE # Токен для телеграм бота
enable_proxy: false # Использовать метод без авторизации при помощи бесплатных прокси true - да, false - нет
API_token_deepinfra: Bearer jwt:aASdsPJKlkjdwlKjs # Если использование прокси отключено вставить апи токен
```
Запукать `main.py`

С параметром `enable_proxy: true` бот может работать долго и нестабильно из-за использования бесплатных `https` прокси
(нужен только для случая когда нельзя получить API для *deepinfra*), 
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

# CHANGELOG

## V0.4.3 - 04:40 15.04.24
Исправленна ошибка с перезапуском бота до окончания диалога в канале и в личных сообщениях

## V0.4.2 - 01:30 15.04.24
Добавлена обработка ошибок ответа с сайта *deepinfra*

## V0.4.1 - 00:35 15.04.24
Исправлен поиск предположительного курса, изменён промт

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
