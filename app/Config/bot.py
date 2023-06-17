import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from app.Middlewares.exceptionHandler import ExceptionHandler

load_dotenv()

bot = AsyncTeleBot(str(os.getenv("MAIN_BOT_TOKEN")), exception_handler=ExceptionHandler())