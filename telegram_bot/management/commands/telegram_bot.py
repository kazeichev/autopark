from abc import ABC
from django.conf import settings

from django.core.management import BaseCommand
from telegram.ext import Updater

import logging

from telegram_bot.handlers.all_handlers import get_all_handlers


class Command(BaseCommand, ABC):
    help = 'Запуск телеграм бота'
    updater = None
    dispatcher = None

    def handle(self, *args, **options):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.set_handlers()

        try:  # TODO прочитать как делать правильно
            self.updater.start_polling()
            while True:
                pass
        except KeyboardInterrupt or Exception:
            self.updater.stop()

    def set_handlers(self):
        all_handlers = get_all_handlers()
        for handler in all_handlers:
            self.dispatcher.add_handler(handler.get_handler())
