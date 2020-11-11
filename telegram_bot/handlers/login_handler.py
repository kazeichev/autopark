from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from telegram_bot.handlers.handler_interface import HandlerInterface

LOGIN_LOGIN, LOGIN_PASSWORD, LOGIN_AUTH = range(3)


class LoginHandler(HandlerInterface):
    name = 'login'
    login = None
    password = None

    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Вы начали процесс авторизации. Продолжить?"
        )

        return LOGIN_LOGIN

    def get_login(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Введите /cancel для того чтобы выйти. \nВведите ваш логин"
        )

        return LOGIN_PASSWORD

    def get_password(self, update, context):
        self.login = update.message.text

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Теперь введите пароль"
        )

        return LOGIN_AUTH

    def auth(self, update, context):
        self.password = update.message.text

        if self.login is None or self.password is None:
            update.message.reply_text(
                'Не введён логин или пароль', reply_markup=ReplyKeyboardRemove()
            )

            return ConversationHandler.END

        user = authenticate(username=self.login, password=self.password)

        if user is None:
            update.message.reply_text(
                'Введён некорректный логин или пароль', reply_markup=ReplyKeyboardRemove()
            )

            return ConversationHandler.END

        user = User.objects.get(username=user)

        update.message.reply_text(
            'Вход успешно осуществлён: \nid: {}\nusername: {}\nlast login: {}'.format(
                user.id, user.username, user.last_login
            ),
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    def cancel(self, update, context):
        update.message.reply_text(
            'Процесс авторизации закончен', reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    def get_handler(self):
        return ConversationHandler(
            entry_points=[CommandHandler(self.name, self.start)],
            states={
                LOGIN_LOGIN: [MessageHandler(Filters.text, self.get_login)],
                LOGIN_PASSWORD: [MessageHandler(Filters.text, self.get_password)],
                LOGIN_AUTH: [MessageHandler(Filters.text, self.auth)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
