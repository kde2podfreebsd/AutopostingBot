import os
import logging
import asyncio
import telebot
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import ForwardFilter

from Bot.Config import bot, inline_menu_manager
from Config import basedir

from Bot.Handlers.mainMenu import send_welcome, _mainMenu
from Bot.Handlers.helpHandler import _helpMenu, _contact, _faq

from Bot.Middlewares.floodingMiddleware import FloodingMiddleware

from Bot.Filters.replyFilter import reply_filter
from Bot.Filters.forwardFilter import forward_filter


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
    @bot.message_handler(func=lambda message: True)
    async def HandlerTextMiddleware(message):

        match message.text:
            case '📖 Помощь':
                await _helpMenu(chat_id=message.chat.id)

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    async def HandlerInlineMiddleware(call):
        print("call data: ", call.data)

        if call.data == "contact":
            await _contact(call)

        if call.data == "faq":
            await _faq(call)

        if call.data == "back_to_main_menu":
            print(inline_menu_manager.help_menu_msgId_to_delete)
            await inline_menu_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
            await _mainMenu(chat_id=call.message.chat.id)

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


if __name__ == "__main__":
    b = Bot()
    asyncio.run(b.polling())
