from aiogram import executor
from ishop.create_bot import dp
from ishop.data_base import sqlite_db
from ishop.handlers import client, admin, application_user


async def on_startup(_):
    print('Бот запущен')
    sqlite_db.connect_to_db()


# Добавлены зарегистрированные хендлеры
client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
application_user.register_handlers_application(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
