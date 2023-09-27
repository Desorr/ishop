import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from ishop.config import API_KEY, PAYMENT_TOKEN
from ishop.data_base import sqlite_db
from ishop.data_base.sqlite_db import get_product_info, get_product_price
from ishop.handlers.application_user import RequestState
from ishop.keyboards import kb_client, ikb_client, ikb_client_iphone11, ikb_client_iphone12, ikb_client_iphone13
from ishop.create_bot import bot
from ishop.utils import RequestData


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать в магазин', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/ishopmain_bot')


# Обычная кнопка доставки
# @dp.message_handler(Text(equals='Доставка', ignore_case=True))
async def shop_open_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Варианты доставки:\n-Самовывоз\n-Европочта\n-Белпочта\n-Автолайтэкспресс')
    await message.delete()


# Обычная кнопка о нас
# @dp.message_handler(Text(equals='О_нас', ignore_case=True))
async def shop_place_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Наше местонахождение:\nБеларусь, г. Минск, ул. Октябрьская, д. 12\n\nРежим работы:\nПн-Вс с 8.00 до 22.00')
    await message.delete()


# Обычная кнопка меню
# @dp.message_handler(Text(equals='Меню', ignore_case=True))
async def shop_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)
    await message.delete()


# Обычная кнопка магазина
# @dp.message_handler(Text(equals='Магазин', ignore_case=True))
async def shop_shop_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите модель iPhone:', reply_markup=ikb_client)
    await message.delete()


# Создаем товар для оплаты + конвертируем цену в тип float
product_info_11 = get_product_info("iPhone 11")
price11 = get_product_price("iPhone 11")
product_info_12 = get_product_info("iPhone 12")
price12 = get_product_price("iPhone 12")
product_info_13 = get_product_info("iPhone 13")
price13 = get_product_price("iPhone 13")


# Инлайн кнопка для отображения информации о iphone 11
# @dp.callback_query_handler(lambda query: query.data == 'iphone11')
async def handle_iphone11(callback_query: CallbackQuery, state: FSMContext):
    product_info = get_product_info("iPhone 11")
    if product_info:
        photo, name, description, price = product_info
        message_text = f'{name}\nОписание: {description}\nЦена: {price} RUB'
        await bot.send_photo(callback_query.from_user.id, photo, message_text, reply_markup=ikb_client_iphone11)
        async with state.proxy() as data:
            data['iphone_price'] = price
    else:
        await callback_query.message.answer("Информация о товаре не найдена.")
    await callback_query.answer()


# Обработка кнопки Купить айфон 11
# @dp.callback_query_handler(lambda query: query.data == 'buy_iphone11')
async def handle_buy_iphone11(callback_query: types.CallbackQuery):
    await callback_query.answer()
    name, description, price = product_info_11[1], product_info_11[2], price11
    price_in_kopecks = int(price * 100)
    await bot.send_invoice(callback_query.from_user.id, name, description, 'invoice_payload_iphone11',
                           PAYMENT_TOKEN, 'RUB', [types.LabeledPrice(name, price_in_kopecks)])


# Инлайн кнопка для отображения информации о iphone 12
# @dp.callback_query_handler(lambda query: query.data == 'iphone12')
async def handle_iphone12(callback_query: CallbackQuery, state: FSMContext):
    product_info = get_product_info("iPhone 12")
    if product_info:
        photo, name, description, price = product_info
        message_text = f'{name}\nОписание: {description}\nЦена: {price} RUB'
        await bot.send_photo(callback_query.from_user.id, photo, message_text, reply_markup=ikb_client_iphone12)
        async with state.proxy() as data:
            data['iphone_price'] = price
    else:
        await callback_query.message.answer("Информация о товаре не найдена.")
    await callback_query.answer()


# Обработка кнопки Купить айфон 12
# @dp.callback_query_handler(lambda query: query.data == 'buy_iphone12')
async def handle_buy_iphone12(callback_query: types.CallbackQuery):
    await callback_query.answer()
    name, description, price = product_info_12[1], product_info_12[2], price12
    price_in_kopecks = int(price * 100)
    await bot.send_invoice(callback_query.from_user.id, name, description, 'invoice_payload_iphone12',
                           PAYMENT_TOKEN, 'RUB', [types.LabeledPrice(name, price_in_kopecks)])


# Инлайн кнопка для отображения информации о iphone 13
# @dp.callback_query_handler(lambda query: query.data == 'iphone13')
async def handle_iphone13(callback_query: CallbackQuery, state: FSMContext):
    product_info = get_product_info("iPhone 13")
    if product_info:
        photo, name, description, price = product_info
        message_text = f'{name}\nОписание: {description}\nЦена: {price} RUB'
        await bot.send_photo(callback_query.from_user.id, photo, message_text, reply_markup=ikb_client_iphone13)
        async with state.proxy() as data:
            data['iphone_price'] = price
    else:
        await callback_query.message.answer("Информация о товаре не найдена.")
    await callback_query.answer()


# Обработка кнопки Купить айфон 13
# @dp.callback_query_handler(lambda query: query.data == 'buy_iphone13')
async def handle_buy_iphone13(callback_query: types.CallbackQuery):
    await callback_query.answer()
    name, description, price = product_info_13[1], product_info_13[2], price13
    price_in_kopecks = int(price * 100)
    await bot.send_invoice(callback_query.from_user.id, name, description, 'invoice_payload_iphone13',
                           PAYMENT_TOKEN, 'RUB', [types.LabeledPrice(name, price_in_kopecks)])


# Бот подтверждает наличие товара
# @dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Обработка при успешной оплате
# @dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def success(message: types.Message):
    await message.answer('Оплата прошла успешно😄')


# Обработка инлайн кнопки Назад
# @dp.callback_query_handler(lambda query: query.data == 'back')
async def handle_back_button(callback_query: CallbackQuery):
    await callback_query.message.answer('Выберите модель iPhone:', reply_markup=ikb_client)
    await callback_query.answer()


# Инлайн кнопка Оставить заявку
async def handle_application_button(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_info = await bot.get_chat(user_id)

    if user_info and user_info.username:
        user_name = user_info.username
    else:
        user_name = "Пользователь"

    async with state.proxy() as data:
        data['name_requested'] = True  # Устанавливаем флаг, что имя не запрашивается, так как оно уже есть
        data['request_data'] = RequestData(user_name, "", "", "",
                                           chat_id)  # Передаем chat_id при создании объекта RequestData

    await RequestState.email.set()  # Устанавливаем состояние "email"
    await state.update_data(user_id=user_id, user_name=user_name)  # Сохраняем ID пользователя и его имя
    await callback_query.answer()
    await callback_query.message.answer(f"Введите вашу электронную почту:")


# Узнать стоимость в долларах API
# @dp.callback_query_handler(lambda query: query.data == 'coursedollar')
async def handler_course(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        iphone_price = float(data['iphone_price'])
    url = 'https://v6.exchangerate-api.com/v6/cc7d0d20fd2988758ca743a2/latest/USD'
    headers = {'apikey': API_KEY}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'conversion_rates' in data:
            conversion_rates = data['conversion_rates']
            if 'RUB' in conversion_rates:
                rub_rate = conversion_rates['RUB']
                iphone_price_usd = iphone_price / rub_rate
                await callback_query.message.answer(f'Актуальный курс доллара: 1 USD = {rub_rate} RUB')
                await callback_query.message.answer(f'Стоимость айфона в долларах: {iphone_price_usd:.2f} USD')
            else:
                await callback_query.message.answer('Курс доллара для RUB не найден.')
        else:
            await callback_query.message.answer('Не удалось получить курс доллара.')
    except Exception as e:
        print(str(e))
        await callback_query.message.answer('Произошла ошибка при получении курса доллара.')


# Хэндлер по оставновке оставления заявки
# @dp.message_handler(state="*", commands='stop')
# @dp.message_handler(Text(equals='stop', ignore_case=True), state="*")
async def stop_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Вы прервали операцию по оставлению заявки")


# Регистрация хендлеров
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(shop_open_command, Text(equals='Доставка', ignore_case=True))
    dp.register_message_handler(shop_place_command, Text(equals='О_нас', ignore_case=True))
    dp.register_message_handler(shop_menu_command, Text(equals='Меню', ignore_case=True))
    dp.register_message_handler(shop_shop_command, Text(equals='Магазин', ignore_case=True))
    dp.register_pre_checkout_query_handler(process_pre_checkout_query)
    dp.register_message_handler(success, content_types=types.ContentType.SUCCESSFUL_PAYMENT)
    dp.register_callback_query_handler(handle_iphone11, lambda query: query.data == 'iphone11')
    dp.register_callback_query_handler(handle_iphone12, lambda query: query.data == 'iphone12')
    dp.register_callback_query_handler(handle_iphone13, lambda query: query.data == 'iphone13')
    dp.register_callback_query_handler(handle_buy_iphone11, lambda query: query.data == 'buy_iphone11')
    dp.register_callback_query_handler(handle_buy_iphone12, lambda query: query.data == 'buy_iphone12')
    dp.register_callback_query_handler(handle_buy_iphone13, lambda query: query.data == 'buy_iphone13')
    dp.register_callback_query_handler(handle_back_button, lambda query: query.data == 'back')
    dp.register_callback_query_handler(handle_application_button, lambda query: query.data == 'application')
    dp.register_message_handler(stop_handler, state="*", commands='stop')
    dp.register_message_handler(stop_handler, Text(equals='stop', ignore_case=True), state="*")
    dp.register_callback_query_handler(handler_course, lambda query: query.data == 'coursedollar')
