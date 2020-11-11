from telegram_bot.handlers.handler_interface import HandlerInterface
from telegram_bot.handlers.login_handler import LoginHandler
from telegram_bot.handlers.repeat_handler import RepeatHandler
from telegram_bot.handlers.report_handler import ReportHandler
from telegram_bot.handlers.start_handler import StartHandler

HANDLERS = [
    StartHandler,
    RepeatHandler,
    LoginHandler,
    ReportHandler
]


def get_all_handlers():
    result = set()

    for handler in HANDLERS:
        if issubclass(handler, HandlerInterface):
            result.add(handler())

    return result
