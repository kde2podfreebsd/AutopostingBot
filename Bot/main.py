import asyncio

from telebot import asyncio_filters  # noqa
from telebot.asyncio_filters import ForwardFilter
from telebot.asyncio_filters import IsDigitFilter
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import StateFilter

from Bot.Config import bot
from Bot.Config import message_context_manager
from Bot.Config import new_chain_manager
from Bot.Handlers.helpMenuHandler import _contact
from Bot.Handlers.helpMenuHandler import _faq
from Bot.Handlers.helpMenuHandler import _helpMenu
from Bot.Handlers.mainMenuHandler import _mainMenu
from Bot.Handlers.newChainHandler import _addNewChain
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
        bot.add_custom_filter(StateFilter(bot))
        bot.add_custom_filter(IsDigitFilter())
        bot.setup_middleware(FloodingMiddleware(1))

    @staticmethod
    @bot.message_handler(func=lambda message: True)
    async def HandlerTextMiddleware(message):

        if message.text == "📖 Помощь":
            await _helpMenu(message)

        if message.text == "🔗 Добавить новую связку":
            new_chain_manager.newChain(chat_id=message.chat.id)
            print(new_chain_manager.chainStore)
            await _addNewChain(message)

        if message.text == "🔙Назад":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )
            await _mainMenu(chat_id=message.chat.id)

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    async def HandlerInlineMiddleware(call):
        print("call data: ", call.data)
        if call.data == "contact":
            await _contact(call)

        if call.data == "faq":
            await _faq(call)

        if call.data == "back_to_main_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _mainMenu(chat_id=call.message.chat.id)

        if call.data == "back_to_new_chain_menu":
            print(new_chain_manager.chainStore)
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await bot.delete_state(call.message.chat.id)
            await _addNewChain(message=call.message)

        if call.data == "new_chain#tg":
            await telegram_source_channel_msg(call.message)
            await bot.set_state(call.message.chat.id, NewChainStates.telegram)

        if call.data == "new_chain#vk":
            await vk_source_channel_msg(call.message)
            await bot.set_state(call.message.chat.id, NewChainStates.vk)

        if call.data == "new_chain#inst":
            await instagram_source_channel_msg(call.message)
            await bot.set_state(call.message.chat.id, NewChainStates.instagram)

        if call.data == "new_chain#continue":
            await bot.send_message(call.message.chat.id, "Укажите телеграм канал канал для постинга")

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
