from telegram.ext import CommandHandler

from telegram_bot.handlers.handler_interface import HandlerInterface


class RepeatHandler(HandlerInterface):
    name = 'repeat'

    @staticmethod
    def get_handler():
        def callback(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text=" ".join(context.args))

        return CommandHandler(RepeatHandler.name, callback)
