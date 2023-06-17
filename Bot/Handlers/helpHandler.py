from Bot.Config import bot, inline_menu_manager
from Bot.Markups.markupBuilder import MarkupBuilder
from telebot import types


async def _helpMenu(chat_id: int | str):
    msg_to_del = await bot.send_message(
        chat_id,
        "⚙️",
        reply_markup=MarkupBuilder.hide_menu,
        parse_mode="MarkdownV2"
    )

    await bot.delete_message(
        chat_id=chat_id,
        message_id=msg_to_del.message_id,
        timeout=0
    )

    msg = await bot.send_message(
        chat_id,
        MarkupBuilder.help_text,
        reply_markup=MarkupBuilder.help_menu(),
        parse_mode="MarkdownV2"
    )

    await inline_menu_manager.add_msgId_to_help_menu_dict(chat_id=chat_id, msgId=msg.message_id)
    print(inline_menu_manager.help_menu_msgId_to_delete)


async def _contact(call: types.CallbackQuery):
    await inline_menu_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
    msg = await bot.send_message(
        call.message.chat.id,
        MarkupBuilder.contact_text,
        reply_markup=MarkupBuilder.help_menu(),
        parse_mode="MarkdownV2"
    )
    await inline_menu_manager.add_msgId_to_help_menu_dict(chat_id=call.message.chat.id, msgId=msg.message_id)


async def _faq(call: types.CallbackQuery):
    await inline_menu_manager.delete_msgId_from_help_menu_dict(chat_id=call.message.chat.id)
    msg = await bot.send_message(
        call.message.chat.id,
        MarkupBuilder.faq_text,
        reply_markup=MarkupBuilder.help_menu(),
        parse_mode="MarkdownV2"
    )
    await inline_menu_manager.add_msgId_to_help_menu_dict(chat_id=call.message.chat.id, msgId=msg.message_id)


