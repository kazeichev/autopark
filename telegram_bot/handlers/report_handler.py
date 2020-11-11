from datetime import date

from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from telegram_bot.handlers.handler_interface import HandlerInterface
from vehicles.models import VehicleMileageReport, Vehicle

REPORT_VEHICLE_ID, REPORT_TYPE, REPORT_FROM_DATE, REPORT_TO_DATE = range(4)


class ReportHandler(HandlerInterface):
    name = 'report'
    vehicle_id = None
    report_type = None
    report_from_date = None
    report_to_date = None

    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Вы начали формировать отчёт. Введите id автомобиля"
        )

        return REPORT_VEHICLE_ID

    def get_vehicle_id(self, update, context):
        self.vehicle_id = update.message.text
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите тип отчёта"
        )

        return REPORT_TYPE

    def get_type(self, update, context):
        self.report_type = update.message.text

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Теперь введите дату начала (yyyy-mm-dd)"
        )

        return REPORT_FROM_DATE

    def get_from_date(self, update, context):
        self.report_from_date = update.message.text

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Теперь введите дату окончания (yyyy-mm-dd)"
        )

        return REPORT_TO_DATE

    def get_to_date(self, update, context):
        self.report_to_date = update.message.text

        if self.vehicle_id is None or self.report_type is None or self.report_from_date is None or self.report_to_date is None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Переданы некорректные данные"
            )

            return ConversationHandler.END

        report = VehicleMileageReport(
            vehicle=Vehicle.objects.get(id=self.vehicle_id),
            period='month' if self.report_type == 'Месяц' else 'year',
            started_at=date.fromisoformat(self.report_from_date),
            finished_at=date.fromisoformat(self.report_to_date),
        )

        report.save()

        update.message.reply_text(
            'Отчёт для автомобиля {}, за {}, с {} по {} \n\n{}'
            .format(
                report.vehicle.vehicle_brand.name,
                self.report_type,
                self.report_from_date,
                self.report_to_date,
                report.result()
            ),
        )

        return ConversationHandler.END

    def cancel(self, update, context):
        update.message.reply_text(
            'Процесс закончен', reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    def get_handler(self):
        return ConversationHandler(
            entry_points=[CommandHandler(self.name, self.start)],
            states={
                REPORT_VEHICLE_ID: [
                    MessageHandler(Filters.text, self.get_vehicle_id)
                ],
                REPORT_TYPE: [MessageHandler(Filters.regex('^(Месяц|Год)$'), self.get_type)],
                REPORT_FROM_DATE: [MessageHandler(Filters.text, self.get_from_date)],
                REPORT_TO_DATE: [MessageHandler(Filters.text, self.get_to_date)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
