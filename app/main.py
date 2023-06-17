import os
import logging
import asyncio
import telebot
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import ForwardFilter

from app.Config import bot
from Config import basedir, logger
from app.Handlers.mainMenu import send_welcome

from app.Middlewares.floodingMiddleware import FloodingMiddleware

from app.Filters.replyFilter import reply_filter
from app.Filters.forwardFilter import forward_filter


class Bot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        bot.add_custom_filter(IsReplyFilter())
        bot.add_custom_filter(ForwardFilter())
        bot.setup_middleware(FloodingMiddleware(1))

    @staticmethod
    async def polling():
        while True:
            try:
                await bot.polling(
                    non_stop=True,
                    interval=0,
                    timeout=20
                )

            except Exception:
                await asyncio.sleep(2)


@bot.message_handler(func=lambda message: True)
async def HandlerTextMiddleware(message):

    match message.text:
        case '📖 Помощь':
            print("kek")


if __name__ == "__main__":
    b = Bot()
    asyncio.run(b.polling())
