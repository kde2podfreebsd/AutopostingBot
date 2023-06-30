from Bot.Config import bot
from Bot.Config import message_context_manager
from Bot.Markups.markupBuilder import MarkupBuilder
from DataBase.DataAccessLayer.UserDAL import UserDAL
from DataBase.session import async_session


async def _mainMenu(message):
    async with async_session() as session:
        async with session.begin():
            user = UserDAL(session)
            status = await user.createUser(chat_id=message.chat.id)
            print(status)
    await bot.delete_state(message.chat.id)
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.welcome_text,
        reply_markup=MarkupBuilder.main_menu(),
        parse_mode="MarkdownV2",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(commands=["help", "start"])
async def send_welcome(message) -> object:
    await _mainMenu(message)
