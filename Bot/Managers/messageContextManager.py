from Bot.Config import bot


class MessageContextManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.help_menu_msgId_to_delete = {}

    async def add_msgId_to_help_menu_dict(self, chat_id, msgId):
        self.help_menu_msgId_to_delete[chat_id] = msgId

    async def delete_msgId_from_help_menu_dict(self, chat_id):
        if self.help_menu_msgId_to_delete[chat_id] is not None:
            await bot.delete_message(chat_id, self.help_menu_msgId_to_delete[chat_id])
            self.help_menu_msgId_to_delete[chat_id] = None
