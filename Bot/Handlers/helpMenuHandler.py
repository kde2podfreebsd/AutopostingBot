from telebot import types

from Bot.Config import bot
from Bot.Config import message_context_manager
from Bot.Markups.markupBuilder import MarkupBuilder


async def _helpMenu(message):
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
        MarkupBuilder.help_text,
        reply_markup=MarkupBuilder.help_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    print(message_context_manager.help_menu_msgId_to_delete)


async def _contact(call: types.CallbackQuery) -> object:
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=call.message.chat.id
    )
    msg = await bot.send_message(
        call.message.chat.id,
        MarkupBuilder.contact_text,
        reply_markup=MarkupBuilder.help_menu(),
        parse_mode="MarkdownV2",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=call.message.chat.id, msgId=msg.message_id
    )


async def _faq(call: types.CallbackQuery):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=call.message.chat.id
    )
    msg = await bot.send_message(
        call.message.chat.id,
        MarkupBuilder.faq_text,
        reply_markup=MarkupBuilder.help_menu(),
        parse_mode="MarkdownV2",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=call.message.chat.id, msgId=msg.message_id
    )
