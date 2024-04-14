import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import re
import pickle


from helper.config import Config

from neirwork.controller import DeepinfraController

logging.basicConfig(level=logging.INFO)
conf = Config()
bot = Bot(conf.get_value('bot_token'))

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class dialog_state(StatesGroup):
    start_dialog = State()
    repl_msg = State()

# ===================================================================
# start reg to bot
@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    """
    Стартовое сообщение для бота, отправляет первую страницу писем
    """
    logging.info('"/start" update dialog with ' + str(message.from_user.id))
    await dialog_state.repl_msg.set()
    nc = DeepinfraController()
    nc.clear_messages()
    await state.update_data(nc=nc)

@dp.message_handler() # Он принимает все запросы без фильтров
async def send_msg(message: types.Message, state: FSMContext):
    """
    Отправляет сообщение без фильтров и используется для старта бота
    """
    logging.info('update dialog with ' + str(message.from_user.id))
    await dialog_state.repl_msg.set()
    nc = DeepinfraController()
    nc.clear_messages()
    nc.add_message(message.text, 'user')
    msg = nc.get_responce()
    await state.update_data(nc=nc)
    if '[' in msg and ']' in msg:
        await state.finish()
    await message.answer(
            text=msg
        )

    
@dp.message_handler(state=dialog_state.repl_msg) # Он принимает все сообщения и отвечает на них
async def send_msg(message: types.Message, state: FSMContext):
    """
    Отправляет сообщение 
    """
    data = await state.get_data()
    nc = data['nc']
    nc.add_message(message.text, 'user')
    logging.info('start message to ' + str(message.from_user.id))
    msg = nc.get_responce()
    await state.update_data(nc=nc)
    if '[' in msg and ']' in msg:
        await state.finish()
    await message.answer(
            text=msg
        )
    
    
@dp.channel_post_handler() # Он принимает все запросы без фильтров
async def send_msg(message: types.Message, state: FSMContext):
    """
    Отправляет сообщение в канал и используется для старта 
    """
    logging.info('drop message chanell ' + str(message.chat.full_name))
    if message.text == '/start':
        logging.info('"/start" message chanell ' + str(message.chat.full_name))
        await dialog_state.repl_msg.set()
        nc = DeepinfraController()
        nc.clear_messages()
        await state.update_data(nc=nc)
        
@dp.channel_post_handler(state=dialog_state.repl_msg) # Он принимает все сообщения в канале для ответа
async def send_msg(message: types.Message, state: FSMContext):
    """
    Отправляет сообщение в канал
    """
    data = await state.get_data()
    nc = data['nc']
    nc.add_message(message.text, 'user')
    logging.info('message chanell ' + str(message.chat.full_name))
    if 'Диалог окончен, accuracy =' in message.text:
        logging.info('stop chanell ' + str(message.chat.full_name))
        nc.clear_messages()
        await state.finish()
    else:
        msg = nc.get_responce()
        await state.update_data(nc=nc)
        if '[' in msg and ']' in msg:
            await state.finish()
        await message.answer(
                text=msg
            )

def main() -> None:  
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    pass
