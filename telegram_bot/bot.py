import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


from helper.config import Config

from neirwork.controller import DeepinfraController

logging.basicConfig(level=logging.INFO)
conf = Config()
bot = Bot(conf.get_value('bot_token'))

USE_PROXY = conf.get_value('enable_proxy')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


nc = DeepinfraController()

# start reg to bot
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Стартовое сообщение для бота, отправляет первую страницу писем
    """

    nc.clear_messages()
    nc.add_message('Привет', 'user')
    logging.info('start message')
    msg = nc.get_responce(use_proxy=USE_PROXY)

    await message.answer(
            text=msg
        )
    
@dp.message_handler() # Он принимает все запросы без фильтров
async def error(message: types.Message):
    """
    Отправляет сообщение об ошибке
    """
    nc.add_message(message.text, 'user')
    logging.info('start message')
    msg = nc.get_responce(use_proxy=USE_PROXY)
    await message.answer(
            text=msg
        )

def main() -> None:  
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    pass
