import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


from helper.config import Config

from neirwork.controller import DeepinfraController
from neirwork.proxy_controller import AvalibleProxies

logging.basicConfig(level=logging.INFO)
conf = Config()
bot = Bot(conf.get_value('bot_token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

pr = AvalibleProxies()
nc = DeepinfraController()

# start reg to bot
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Стартовое сообщение для бота, отправляет первую страницу писем
    """

    nc.clear_messages()
    nc.add_message('Привет', 'user')
    proxies = pr.get_available_proxies()
    while proxies == []:
        print('another')
        pr.update_proxies()
        proxies = pr.get_available_proxies()
    proxies = pr.ip_to_proxy(proxies[0])
    msg = nc.get_responce(proxies=proxies)

    await message.answer(
            text=msg
        )
    
@dp.message_handler() # Он принимает все запросы без фильтров
async def error(message: types.Message):
    """
    Отправляет сообщение об ошибке
    """
    nc.add_message(message.text, 'user')
    proxies = pr.get_available_proxies()
    while proxies == []:
        print('another')
        pr.update_proxies()
        proxies = pr.get_available_proxies()
        print(proxies)
    proxies = pr.ip_to_proxy(proxies[0])
    msg = nc.get_responce(proxies=proxies)
    await message.answer(
            text=msg
        )

def main() -> None:  
    executor.start_polling(dp, skip_updates=True)
    
if __name__ == '__main__':
    pass
