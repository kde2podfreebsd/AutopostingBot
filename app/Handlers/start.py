from app.Config import bot
from app.Keyboards.MainMenu import welcome_text, main_menu


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message: object) -> object:
    await bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=main_menu,
        parse_mode="MARKDOWN"
    )


# @bot.message_handler(func=lambda message: True)
# async def echo_message(message):
#     await bot.reply_to(message, message.text)

