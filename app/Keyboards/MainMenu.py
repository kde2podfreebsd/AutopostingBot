from telebot import types
from telebot.types import ReplyKeyboardMarkup

welcome_text: str = '''\
👋 Приветствую вас в нашем боте! Вы можете добавить новую связку для парсинга и постинга контента, управлять текущими связками, оплатить подписку или получить помощь.
'''

main_menu: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
