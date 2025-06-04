from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import telegram_token

bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class Status(StatesGroup):
    lolzteam = State()
    rukassa = State()
