import logging

import telebot

logging.getLogger(__name__)


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        telebot.logger.error(exception)
        logging.error(telebot.logger.error(exception))
        print("ERROR: ", {exception})
