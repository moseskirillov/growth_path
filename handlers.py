import logging

from telegram import Update

from database.db_connect import connection
from models.user_model import User


async def start(update: Update, _):
    logging.info('Обработка команды старт')
    with connection.atomic():
        user, create = User.get_or_create(
            telegram_id=update.effective_message.from_user.id,
            defaults={
                'first_name': update.effective_chat.first_name,
                'last_name': update.effective_chat.last_name,
                'telegram_login': update.effective_chat.username
            }
        )
        if create:
            logging.info(f'Создан новый пользователь: {user.first_name} {user.last_name}')
    await update.message.reply_text(
        text=f'Привет, {update.effective_chat.first_name}!\n'
             f'Для нужного действия нажми на одну из кнопок внизу',
    )
