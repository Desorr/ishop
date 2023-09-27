from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура админа
button_load = KeyboardButton('Загрузить')
button_delete = KeyboardButton('Удалить')
button_back_to_user = KeyboardButton('Выйти_из_режима_модератора')


button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete).add(button_back_to_user)
