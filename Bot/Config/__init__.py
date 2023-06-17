from .bot import bot
import os
from dotenv import load_dotenv
import telebot
import logging

basedir = f'{os.path.abspath(os.path.dirname(__file__))}/../'
load_dotenv()
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

# logging.basicConfig(
#     filename=f'{basedir}/Logs/logs.log',
#     filemode='a',
#     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#     datefmt='%H:%M:%S',
#     level=logging.DEBUG
# )

from Bot.Middlewares.InlineMenuManager import InlineMenuManager
inline_menu_manager = InlineMenuManager()
