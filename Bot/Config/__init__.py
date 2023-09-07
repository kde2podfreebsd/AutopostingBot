# import logging # noqa
import os

from telebot.callback_data import CallbackData

from .bot import bot  # noqa

# import telebot # noqa
# from dotenv import load_dotenv # noqa

basedir = f"{os.path.abspath(os.path.dirname(__file__))}/../"

provider_token = os.getenv("PROVIDER_YOOKASSA_TEST")

# load_dotenv()
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)
#
# logging.basicConfig(
#     filename=f"{basedir}/Logs/logs.log",
#     filemode="a",
#     format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
#     datefmt="%H:%M:%S",
#     level=logging.DEBUG,
# )

from Bot.Managers.messageContextManager import MessageContextManager
from Bot.Managers.newChainManager import NewChainManager

message_context_manager = MessageContextManager()
new_chain_manager = NewChainManager()

invoice_factory = CallbackData('product_id', prefix='products')
