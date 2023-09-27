from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from ishop.create_bot import bot, dp
from ishop.data_base import sqlite_db
from ishop.handlers.client import command_start
from ishop.keyboards import admin_kb, client_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Состояния
class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Получить список администраторов группы
async def get_admin_ids(chat_id):
    chat_admins = await bot.get_chat_administrators(chat_id)
    return [admin.user.id for admin in chat_admins]


# Проверка на админа
# @dp.message_handler(commands=['admin'])
async def make_changes_command(message: types.Message):
    chat_id = message.chat.id
    admin_ids = await get_admin_ids(chat_id)
    if message.from_user.id in admin_ids:
        await bot.send_message(message.from_user.id, "Вы администратор и имеете доступ к меню модератора.",
                               reply_markup=admin_kb.button_case_admin)
        await message.delete()
    else:
        await bot.send_message(message.from_user.id, "Вы обычный пользователь.", reply_markup=client_kb.kb_client)
        await message.delete()


# Обработчик команды /Выйти_из_режима_модератора
# @dp.message_handler(Text(equals='Выйти_из_режима_модератора', ignore_case=True))
async def exit_moderator_mode(message: types.Message):
    await bot.set_my_commands([])
    await bot.send_message(message.from_user.id, 'Режима модератора деактивирован')
    dp.register_message_handler(command_start, commands=['start', 'help'])
    await command_start(message)


# Начало диалога загрузки нового пункта меню
# @dp.message_handler(Text(equals='Загрузить', ignore_case=True), state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Добавить фото')


# Выход из состояний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Загрузка контента отменена")


# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Название товара")


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Описание товара")


# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply("Цена товара")


# Ловим последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await sqlite_db.sql_add_command(data)
    await bot.send_message(message.from_user.id, text='Товар успешно добавлен!')
    await state.finish()


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


# @dp.message_handler(Text(equals='Удалить', ignore_case=True))
async def delete_item(message: types.Message):
    read = await sqlite_db.sql_read2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-2]}')
        await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


# Регистрация хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, Text(equals='Загрузить', ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_item, Text(equals='Удалить', ignore_case=True))
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(make_changes_command, commands='admin')
    dp.register_message_handler(exit_moderator_mode, Text(equals='Выйти_из_режима_модератора', ignore_case=True))
