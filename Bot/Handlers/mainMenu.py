from Bot.Config import bot
from Bot.Markups.markupBuilder import MarkupBuilder


async def _mainMenu(chat_id: int | str):
    await bot.send_message(
        chat_id,
        MarkupBuilder.welcome_text,
        reply_markup=MarkupBuilder.main_menu(),
        parse_mode="MarkdownV2"
    )


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message) -> object:
    await _mainMenu(chat_id=message.chat.id)

