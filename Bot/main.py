import asyncio

from telebot import asyncio_filters
from telebot.asyncio_filters import ForwardFilter
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import StateFilter

from Bot.Config import bot
from Bot.Config import inline_menu_manager
from Bot.Handlers.helpMenuHandler import _contact
from Bot.Handlers.helpMenuHandler import _faq
from Bot.Handlers.helpMenuHandler import _helpMenu
from Bot.Handlers.mainMenuHandler import _mainMenu
from Bot.Handlers.newChainHandler import _addNewChain
from Bot.Handlers.newChainHandler import get_instagram_source_profile
from Bot.Handlers.newChainHandler import get_telegram_source_channel
from Bot.Handlers.newChainHandler import get_vk_source_profile
from Bot.Handlers.newChainHandler import instagram_source_channel_msg
from Bot.Handlers.newChainHandler import NewChainStates
from Bot.Handlers.newChainHandler import telegram_source_channel_msg
from Bot.Handlers.newChainHandler import vk_source_channel_msg
from Bot.Middlewares.floodingMiddleware import FloodingMiddleware


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
        bot.add_custom_filter(asyncio_filters.StateFilter(bot))
        bot.add_custom_filter(asyncio_filters.IsDigitFilter())

    @staticmethod
    @bot.message_handler(func=lambda message: True)
    async def HandlerTextMiddleware(message):

        if message.text == "📖 Помощь":
            await _helpMenu(chat_id=message.chat.id)

        if message.text == "🔗 Добавить новую связку":
            await _addNewChain(message)

        if message.text == "🔙Назад":
            await inline_menu_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )
            await _mainMenu(chat_id=message.chat.id)

        if message.text == "📡 Телеграм канал":
            await telegram_source_channel_msg(message=message)
            await bot.set_state(
                message.from_user.id, NewChainStates.telegram, message.chat.id
            )

        if message.text == "📸 Instagram страница":
            await instagram_source_channel_msg(message=message)
            await bot.set_state(
                message.from_user.id, NewChainStates.instagram, message.chat.id
            )

        if message.text == "🌐 ВК-паблик":
            await vk_source_channel_msg(message=message)
            await bot.set_state(
                message.from_user.id, NewChainStates.vk, message.chat.id
            )

        if message.text == "➡️Продолжить":
            await bot.set_state(
                message.from_user.id, NewChainStates.sourceTgChannel, message.chat.id
            )

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    async def HandlerInlineMiddleware(call):
        print("call data: ", call.data)

        if call.data == "contact":
            await _contact(call)

        if call.data == "faq":
            await _faq(call)

        if call.data == "back_to_main_menu":
            await inline_menu_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _mainMenu(chat_id=call.message.chat.id)

        if call.data == "back_to_new_chain_menu":
            await inline_menu_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await bot.delete_state(call.message.chat.id)
            await _addNewChain(message=call.message)

    @staticmethod
    async def polling():
        while True:
            try:
                await bot.polling(non_stop=True, interval=0, timeout=20)

            except Exception:
                await asyncio.sleep(2)


if __name__ == "__main__":
    b = Bot()
    asyncio.run(b.polling())
