import asyncio
from app.Config import bot
from app.Handlers.start import send_welcome
# from app.Handlers.FAQ.faq import


def on_startup():
    pass


if __name__ == "__main__":
    asyncio.run(bot.polling())