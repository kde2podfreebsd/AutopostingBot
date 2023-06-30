import re

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from Bot.Config import bot
from Bot.Config import message_context_manager
from Bot.Config import new_chain_manager
from Bot.Markups.markupBuilder import MarkupBuilder
import datetime


class NewChainStates(StatesGroup):
    addNewChain = State()
    telegram = State()
    instagram = State()
    vk = State()
    sourceTgChannel = State()
    setTarget = State()
    setParsingType = State()
    setParsingTime = State()


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
        MarkupBuilder.current_chain_menu_text(chat_id=message.chat.id),
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
        reply_markup=MarkupBuilder.back_to_chain_menu(),
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
        status = new_chain_manager.add_source_url(
            chat_id=message.chat.id, source_url=data["tg"], source_type="telegram"
        )
        if status is True:
            print(new_chain_manager.chainStore)
            await bot.delete_state(message.from_user.id)
            await _addSourceToCurrentChain(message)
        elif status is False:
            msg = await bot.send_message(
                message.chat.id,
                MarkupBuilder.error_duplicate_source_url_toChain,
                reply_markup=MarkupBuilder.back_to_chain_menu(),
                parse_mode="MarkdownV2",
            )

            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, msgId=msg.message_id
            )

        elif status == "MaxSize":
            msg = await bot.send_message(
                message.chat.id,
                MarkupBuilder.error_maxSize_toChain,
                reply_markup=MarkupBuilder.back_to_chain_menu(),
                parse_mode="MarkdownV2",
            )

            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, msgId=msg.message_id
            )

    else:
        msg = await bot.send_message(
            message.chat.id,
            MarkupBuilder.error_in_add_url_toChain,
            reply_markup=MarkupBuilder.back_to_chain_menu(),
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
        reply_markup=MarkupBuilder.back_to_chain_menu(),
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
        reply_markup=MarkupBuilder.back_to_chain_menu(),
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


async def setTargetChannel(message):

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.setTargetChannel(chat_id=message.chat.id),
        reply_markup=MarkupBuilder.back_to_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(state=NewChainStates.setTarget)
async def setTarget(message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message_context_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    pattern = r"^@[\w-]+$"

    if re.match(pattern, message.text):

        new_chain_manager.add_target_channel(
            chat_id=message.chat.id, channel=message.text
        )

        msg = await bot.send_message(
            message.chat.id,
            MarkupBuilder.setParsingType,
            reply_markup=MarkupBuilder.parsingTypeMenu(),
            parse_mode="MarkdownV2",
        )

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )

        await bot.set_state(message.chat.id, NewChainStates.setParsingType)

    else:
        msg = await bot.send_message(
            message.chat.id,
            MarkupBuilder.error_in_add_url_toChain,
            reply_markup=MarkupBuilder.back_to_chain_menu(),
            parse_mode="MarkdownV2",
        )

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )


@bot.message_handler(state=NewChainStates.setParsingType)
async def setParsingType(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message_context_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    msg = await bot.send_message(
        chat_id=message.chat.id,
        text=MarkupBuilder.setParsingType,
        reply_markup=MarkupBuilder.parsingTypeMenu,
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


async def setParsingOldType(message):
    msg = await bot.send_message(
        chat_id=message.chat.id,
        text=MarkupBuilder.setParsingOldTypeText,
        reply_markup=MarkupBuilder.setParsingOldType(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


async def setPostSchedule(message, parsing_type):

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.setTime(parsing_type=parsing_type),
        reply_markup=MarkupBuilder.back_to_chain_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(state=NewChainStates.setParsingTime)
async def setParsingTime(message):

    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message_context_manager.help_menu_msgId_to_delete[message.chat.id],
        timeout=0,
    )

    def check_hours_format(time_string: str):
        pattern = r'^\d{2}:\d{2}(\|\d{2}:\d{2})*$'

        if not re.match(pattern, time_string):
            return False

        hours = []
        time_list = time_string.split('|')

        for time in time_list:
            hour, minute = time.split(':')
            hour = int(hour)
            minute = int(minute)

            if minute > 59 or hour > 23 or hour < 0 or minute < 0:
                return False

            hour_string = f'{hour:02d}:{minute:02d}'
            hours.append(hour_string)

        return hours

    status = check_hours_format(time_string=message.text)

    if status is False:
        pass
    else:

        new_chain_manager.add_parsing_time(
            chat_id=message.chat.id,
            time_list=status
        )

        msg = await bot.send_message(
            chat_id=message.chat.id,
            text=MarkupBuilder.setAdditionalText(time_list=status),
            reply_markup=MarkupBuilder.back_to_timeSetter()
        )

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )


async def confirmNewChainText(message):

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.confirmNewChainText(chat_id=message.chat.id),
        reply_markup=MarkupBuilder.confirmNewChain(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
