import os

from dotenv import load_dotenv

from .bot import bot  # noqa

basedir = f"{os.path.abspath(os.path.dirname(__file__))}/../"

load_dotenv()
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
