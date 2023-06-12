import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

bot: AsyncTeleBot = AsyncTeleBot(str(os.getenv("MAIN_BOT_TOKEN")))

POSTGRES_URL: str = f'postgresql+asyncpg://{str(os.getenv("DATABASE_USER"))}:{str(os.getenv("DATABASE_PASSWORD"))}@{str(os.getenv("DATABASE_HOST"))}:{str(os.getenv("DATABASE_PORT"))}/{str(os.getenv("DATABASE_NAME"))}'
