import re

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from Bot.Config import bot
from Bot.Config import message_context_manager
from Bot.Config import new_chain_manager
from Bot.Markups.markupBuilder import MarkupBuilder


class NewChainStates(StatesGroup):
    addNewChain = State()
    telegram = State()
    instagram = State()
    vk = State()
    sourceTgChannel = State()


async def _addNewChain(message):
    msg_to_del = await bot.send_message(
        message.chat.id,
        "⚙️",
        reply_markup=MarkupBuilder.hide_menu,
        parse_mode="MarkdownV2",
    )

    await bot.delete_message(
        chat_id=message.chat.id, message_id=msg_to_del.message_id, timeout=0
    )

    new_chain_manager.newChain(chat_id=message.chat.id)

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.new_chain_menu_text,
        reply_markup=MarkupBuilder.new_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


async def _addSourceToCurrentChain(message):
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
        reply_markup=MarkupBuilder.current_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


async def telegram_source_channel_msg(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message_context_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.create_new_telegram_chain_text,
        reply_markup=MarkupBuilder.back_to_new_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(state=NewChainStates.telegram)
async def get_telegram_source_channel(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message_context_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    pattern = r"^@[\w-]+$"

    if re.match(pattern, message.text):
        await bot.send_message(message.chat.id, "Telegram")
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["tg"] = message.text
        # new_chain_manager.add_source_url(
        #     chat_id=message.chat.id, source_url=data["tg"], source_type="telegram"
        # )
        await bot.delete_state(message.from_user.id)
        await _addSourceToCurrentChain(message)

    else:
        msg = await bot.send_message(
            message.chat.id,
            MarkupBuilder.error_in_add_url_toChain,
            reply_markup=MarkupBuilder.back_to_new_chain_menu(),
            parse_mode="MarkdownV2",
        )

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )


async def instagram_source_channel_msg(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message_context_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.create_new_instagram_chain_text,
        reply_markup=MarkupBuilder.back_to_new_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(state=NewChainStates.instagram)
async def get_instagram_source_channel(message):
    await bot.send_message(message.chat.id, "Instagram")
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text
    await bot.delete_state(message.from_user.id)
    await _addSourceToCurrentChain(message)


async def vk_source_channel_msg(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message_context_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.create_new_vk_chain_text,
        reply_markup=MarkupBuilder.back_to_new_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(state=NewChainStates.vk)
async def get_vk_source_channel(message):
    await bot.send_message(message.chat.id, "VK")
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text
    await bot.delete_state(message.from_user.id)
    await _addSourceToCurrentChain(message)
