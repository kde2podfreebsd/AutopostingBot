from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from Bot.Config import bot
from Bot.Config import inline_menu_manager
from Bot.Markups.markupBuilder import MarkupBuilder


class NewChainStates(StatesGroup):
    addNewChain = State()
    telegram = State()
    instagram = State()
    vk = State()
    sourceTgChannel = State()


async def _addNewChain(message):
    await bot.delete_state(message.from_user.id)
    msg_to_del = await bot.send_message(
        message.chat.id,
        "⚙️",
        reply_markup=MarkupBuilder.hide_menu,
        parse_mode="MarkdownV2",
    )

    await bot.delete_message(
        chat_id=message.chat.id, message_id=msg_to_del.message_id, timeout=0
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.new_chain_menu_text,
        reply_markup=MarkupBuilder.new_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await inline_menu_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(state=NewChainStates.telegram)
async def get_telegram_source_channel(message):
    await bot.send_message(message.chat.id, "Telegram")
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text
    await bot.delete_state(message.from_user.id)
    await _addNewChain(message)


async def telegram_source_channel_msg(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=inline_menu_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.create_new_telegram_chain_text,
        reply_markup=MarkupBuilder.back_to_new_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await inline_menu_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(state=NewChainStates.instagram)
async def get_instagram_source_profile(message):
    await bot.send_message(message.chat.id, "Instagram")
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text
    print(data, message.text)
    await bot.delete_state(message.from_user.id)
    await _addNewChain(message)


async def instagram_source_channel_msg(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=inline_menu_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.create_new_instagram_chain_text,
        reply_markup=MarkupBuilder.back_to_new_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await inline_menu_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(state=NewChainStates.vk)
async def get_vk_source_profile(message):
    await bot.send_message(message.chat.id, "VK")
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text
    print(data, message.text)
    await bot.delete_state(message.from_user.id)
    await _addNewChain(message)


async def vk_source_channel_msg(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=inline_menu_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.create_new_vk_chain_text,
        reply_markup=MarkupBuilder.back_to_new_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await inline_menu_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
