import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from Bot.Middlewares.exceptionHandler import ExceptionHandler

load_dotenv()

bot = AsyncTeleBot(
    str(os.getenv("MAIN_BOT_TOKEN")),
    exception_handler=ExceptionHandler(),
    state_storage=StateMemoryStorage(),
)
