import sqlite3 as sq

import aiosqlite

from ishop.create_bot import bot
from ishop.keyboards import ikb_client


def connect_to_db():
    base = sq.connect('ishop1.db')
    cur = base.cursor()
    if base:
        print('Database connected OK')
    return base, cur


def create_tables(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            img TEXT,
            name TEXT PRIMARY KEY,
            description TEXT,
            price TEXT,
            timestamp DATETIME
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            comment TEXT,
            chat_id TEXT
        )
    ''')


base, cur = connect_to_db()
create_tables(cur)


# Получить уникальные chat_id из базы данных
async def get_unique_chat_ids_from_database():
    try:
        async with aiosqlite.connect('ishop1.db') as conn:
            cursor = await conn.cursor()
            await cursor.execute('SELECT DISTINCT chat_id FROM requests')
            unique_chat_ids = [row[0] for row in await cursor.fetchall()]
            return unique_chat_ids
    except Exception as e:
        print(f"Ошибка при получении уникальных chat_id пользователей с заявками: {str(e)}")
        return []


# Добавляем контент с уведомлением всех уникальных пользователей
async def sql_add_command(data):
    cur.execute('INSERT INTO menu (img, name, description, price, timestamp) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)',
                (data['photo'], data['name'], data['description'], data['price']))
    base.commit()
    unique_chat_ids = await get_unique_chat_ids_from_database()
    message_text = f"Поступил новый {data['name']}🚀\nУже в магазине👇"
    for chat_id in unique_chat_ids:
        await bot.send_message(chat_id, message_text, reply_markup=ikb_client)


# Посмотреть весь контент
async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-2]} RUB')


# Посмотреть весь контент для удаления
async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


# Получить информацию о товаре
def get_product_info(name):
    cur.execute('SELECT img, name, description, price FROM menu WHERE name = ?', (name,))
    product_info = cur.fetchone()
    return product_info


# Получить цену товара в типе Float
def get_product_price(name):
    cur.execute("SELECT price FROM menu WHERE name=?", (name,))
    result = cur.fetchone()
    if result:
        price_text = result[0]
        try:
            price = float(price_text)
            return price
        except ValueError:
            print(f"Ошибка конвертации цены '{price_text}' в тип float.")
            return None


# Удалить объект из контента
async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()


# Добавить заявку от клиента в бд
async def add_request(data):
    cur.execute('INSERT INTO requests (name, email, phone, comment, chat_id) VALUES (?, ?, ?, ?, ?)',
                (data.name, data.email, data.phone, data.comment, data.chat_id))
    base.commit()
