from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from ishop.config import BOT_TOKEN

storage = MemoryStorage()

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
