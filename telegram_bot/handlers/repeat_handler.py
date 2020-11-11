from telegram.ext import CommandHandler

from telegram_bot.handlers.handler_interface import HandlerInterface


class RepeatHandler(HandlerInterface):
    name = 'repeat'

    def callback(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=" ".join(context.args))

    def get_handler(self):
        return CommandHandler(self.name, self.callback)
