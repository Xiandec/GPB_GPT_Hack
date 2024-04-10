import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import re


from helper.config import Config

from neirwork.controller import DeepinfraController

logging.basicConfig(level=logging.INFO)
conf = Config()
bot = Bot(conf.get_value('bot_token'))

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

    
@dp.message_handler() # Он принимает все запросы без фильтров
async def send_msg(message: types.Message):
    """
    Отправляет сообщение 
    """
    nc.add_message(message.text, 'user')
    logging.info('start message')
    msg = nc.get_responce()
    
    await message.answer(
            text=msg
        )
    
@dp.channel_post_handler() # Он принимает все запросы без фильтров
async def send_msg(message: types.Message):
    """
    Отправляет сообщение 
    """
    nc.add_message(message.text, 'user')
    logging.info('start message chanell')
    if message.text == '/start':
        logging.info('update chanell')
        nc.clear_messages()
    elif 'Диалог окончен, accuracy =' in message.text:
        logging.info('stop chanell')
        nc.clear_messages()
    else:
        msg = nc.get_responce()
        
        await message.answer(
                text=msg
            )

def main() -> None:  
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    pass
