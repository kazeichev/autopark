from abc import ABC

from telegram.ext import CommandHandler

from telegram_bot.handlers.handler_interface import HandlerInterface


class StartHandler(HandlerInterface, ABC):
    name = 'start'

    @staticmethod
    def get_handler():
        def callback(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Это бот автопарка!")

        return CommandHandler(StartHandler.name, callback)
