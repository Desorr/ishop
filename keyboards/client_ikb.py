from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b1 = InlineKeyboardButton(text='iPhone 11', callback_data='iphone11')
b2 = InlineKeyboardButton(text='iPhone 12', callback_data='iphone12')
b3 = InlineKeyboardButton(text='iPhone 13', callback_data='iphone13')

ikb_client = InlineKeyboardMarkup(row_width=1)
ikb_client.add(b1, b2, b3)
