from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b1 = InlineKeyboardButton(text='Купить iphone 11', callback_data='buy_iphone11')
b2 = InlineKeyboardButton(text='Оставить заявку', callback_data='application')
b3 = InlineKeyboardButton(text='Цена в $', callback_data='coursedollar')
b4 = InlineKeyboardButton(text='Назад', callback_data='back')

ikb_client_iphone11 = InlineKeyboardMarkup(row_width=1)
ikb_client_iphone11.add(b1, b2, b3, b4)
