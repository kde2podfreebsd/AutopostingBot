import logging
import os

import telebot
from dotenv import load_dotenv

from .bot import bot  # noqa

basedir = f"{os.path.abspath(os.path.dirname(__file__))}/../"
load_dotenv()
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

logging.basicConfig(
    filename=f"{basedir}/Logs/logs.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

from Bot.Middlewares.InlineContextManager import InlineContextManager

inline_menu_manager = InlineContextManager()
