import logging
import os

from telegram.ext import ApplicationBuilder, CommandHandler

from config import logging_init
from database.db_init import database_init
from handlers import start

TOKEN = os.getenv('BOT_TOKEN')


def main():
    logging.info('Старт бота')
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(CommandHandler('start', start))
    bot.run_polling()


if __name__ == '__main__':
    logging_init()
    database_init()
    main()
