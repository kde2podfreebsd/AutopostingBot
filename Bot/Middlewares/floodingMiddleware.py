from Bot.Config import bot
from telebot.asyncio_handler_backends import BaseMiddleware
from telebot.asyncio_handler_backends import CancelUpdate


class FloodingMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        super().__init__()
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']

    async def pre_process(self, message, data):
        if not message.from_user.id in self.last_time:
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            await bot.send_message(message.chat.id, 'Вы делаете запросы слишком часто')
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date

    async def post_process(self, message, data, exception):
        pass
        # await bot.send_message(message.chat.id, 'text')