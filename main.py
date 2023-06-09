import logging
import os

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from config import logging_init
from database.db_init import database_init
from services.handlers import start_handler, register_to_meeting_handler, \
    mark_a_visitor_handler, cancel_registration_handler, check_my_registration_handler, get_qr_code_handler, \
    select_meeting_type_handler, find_next_step_handler
from services.keyboards import STEP_REGISTER_CALLBACK, RETURN_CALLBACK

TOKEN = os.getenv('BOT_TOKEN')


def main():
    logging.info('Старт бота')
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(CommandHandler('start', start_handler))
    bot.add_handler(MessageHandler(filters.Text(['Вернуться']), start_handler))
    bot.add_handler(MessageHandler(filters.Text(['Зарегистрироваться']), select_meeting_type_handler))
    bot.add_handler(MessageHandler(filters.Text(['Первые шаги']), find_next_step_handler))
    bot.add_handler(MessageHandler(filters.Text(['Мои регистрации']), check_my_registration_handler))
    bot.add_handler(MessageHandler(filters.Text(['Отменить регистрацию']), cancel_registration_handler))
    bot.add_handler(MessageHandler(filters.Text(['Получить QR код']), get_qr_code_handler))
    bot.add_handler(MessageHandler(filters.PHOTO, mark_a_visitor_handler))
    bot.add_handler(CallbackQueryHandler(register_to_meeting_handler, pattern=STEP_REGISTER_CALLBACK))
    bot.add_handler(CallbackQueryHandler(start_handler, pattern=RETURN_CALLBACK))
    bot.run_webhook(
        listen='0.0.0.0',
        port=5001,
        url_path='growth',
        webhook_url='https://1493881-cr74590.tw1.ru/growth',
    )


if __name__ == '__main__':
    logging_init()
    database_init()
    main()
