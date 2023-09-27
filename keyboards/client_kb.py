from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Клавиатура стартовая
b1 = KeyboardButton('Доставка')
b2 = KeyboardButton('О_нас')
b3 = KeyboardButton('Меню')
b4 = KeyboardButton('Магазин')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b3, b4).row(b1, b2)
