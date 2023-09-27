from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from ishop.create_bot import bot
from ishop.data_base.sqlite_db import add_request


# Состояния
class RequestState(StatesGroup):
    name = State()
    email = State()
    phone = State()
    comment = State()


# Получаем почту и переходим к номеру телефона
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['request_data'].email = message.text
    await RequestState.next()
    await message.reply("Введите ваш номер телефона:")


# Получаем номер телефона и переходим к комментарию
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['request_data'].phone = message.text
    await RequestState.next()
    await message.reply("Добавьте комментарий:")


# Получаем комментарий и добавляем в БД
async def process_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['request_data'].comment = message.text
        await add_request(data['request_data'])
        print(
            f"Data to be added: {data['request_data'].__dict__}")  # Проверка в консоли данных, которые добавляются в БД
    await bot.send_message(message.from_user.id, text='Заявка успешно отправлена')
    await state.finish()


# Регистация хэндлеров
def register_handlers_application(dp: Dispatcher):
    dp.register_message_handler(process_email, state=RequestState.email)
    dp.register_message_handler(process_phone, state=RequestState.phone)
    dp.register_message_handler(process_comment, state=RequestState.comment)
