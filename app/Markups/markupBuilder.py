from telebot import types
from telebot.types import ReplyKeyboardMarkup
from telebot import formatting


class MarkupBuilder:
    _welcome_text: object | None = None
    _hide_menu: object | None = None

    @classmethod
    def main_menu(cls):
        menu: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=True,
        ).add(
            types.KeyboardButton("🔗 Добавить новую связку"),
            types.KeyboardButton("💳 Оплатить подписку"),
            types.KeyboardButton("📋 Мои связки"),
            types.KeyboardButton("📖 Помощь")
        )
        return menu

    @classmethod
    @property
    def welcome_text(cls):
        cls._welcome_text: object = formatting.format_text(
            formatting.mbold('👋Приветствую вас в нашем боте!'),
            "\nВы можете добавить новую связку для парсинга и постинга контента, управлять текущими связками, оплатить подписку или получить помощь\.",
            separator=""
        )
        return cls._welcome_text


    @classmethod
    @property
    def hide_menu(cls):
        cls._hide_menu: object = types.ReplyKeyboardRemove()
        return cls._hide_menu


