import logging
import os
import random
import string

import qrcode
from PIL import Image
from pyzbar import pyzbar
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from services.data_service import get_or_create_user, get_next_meeting, register_to_meeting, mark_a_visitor, \
    find_user_by_id, cancel_registration, check_registration, delete_registration, get_current_registration
from services.keyboards import start_keyboard, register_to_meeting_keyboard, cancel_registration_keyboard

GO_TO_LOGIN_TEXT = 'Вы не залогинены. Для логина, сначала нажмите /start'


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('Обработка команды старт')
    if context.user_data.get('user_id') is None:
        user = get_or_create_user(
            telegram_id=update.effective_message.from_user.id,
            first_name=update.effective_chat.first_name,
            last_name=update.effective_chat.last_name,
            telegram_login=update.effective_chat.username
        )
        context.user_data['user_id'] = user.id
    await update.message.reply_text(
        text=f'Привет, {update.effective_chat.first_name}!\n'
             f'Чтобы зарегистрироваться на встречу,\n'
             f'нажми на кнопку внизу',
        reply_markup=start_keyboard
    )


async def find_next_meeting_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('Обработка команды поиска следующей встречи')
    user_id = context.user_data.get('user_id')
    if user_id:
        next_meeting = get_next_meeting(user_id)
        keyboard = register_to_meeting_keyboard
        if next_meeting:
            context.user_data['next_meeting'] = next_meeting.meetingdate.id
            formatted_date = next_meeting.meetingdate.date.strftime('%d.%m.%Y %H:%M')
            response_message = f'<b>Ближайшая встреча</b>: {next_meeting.title}\n' \
                               f'<b>Дата проведения</b>: {formatted_date}'
        else:
            keyboard = start_keyboard
            response_message = 'На данный момент нет доступных встреч'
        await update.message.reply_text(
            text=response_message,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(text=GO_TO_LOGIN_TEXT)


async def register_to_meeting_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('Обработка команды регистрации на встречу')
    user_id = context.user_data.get('user_id')
    await update.callback_query.answer()
    if user_id:
        meeting_id = context.user_data.get('next_meeting')
        if meeting_id is None:
            next_meeting = get_next_meeting(user_id)
            meeting_id = next_meeting.meetingdate.id
        register, created = register_to_meeting(user_id=user_id, meeting_id=meeting_id)
        file_path = generate_qr_code(register.id)
        if created:
            success_response_message = 'Вы успешно зарегистрированы, данный QR код ' \
                                       'необходимо будет показать при входе на встречу:'
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=success_response_message,
                parse_mode=ParseMode.HTML,
                reply_markup=cancel_registration_keyboard
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы уже зарегистрированы на эту встречу, вот QR код',
                reply_markup=cancel_registration_keyboard
            )
        with open(file_path, 'rb') as qr_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_file
            )
        os.remove(file_path)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=GO_TO_LOGIN_TEXT
        )


async def mark_a_visitor_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id')
    if user_id:
        user = find_user_by_id(user_id)
        if user.is_admin:
            qr = await update.message.photo[-1].get_file()
            file_path = f'{generate_random_filename()}.png'
            await qr.download_to_drive(f'{file_path}')
            registration_id = read_qr_code(file_path)
            register_result = mark_a_visitor(registration_id)
            delete_registration(registration_id)
            os.remove(file_path)
            await update.message.reply_text(
                text=register_result
            )
        else:
            await update.message.reply_text(text='У тебя нет прав на эту команду')
    else:
        await update.message.reply_text(text=GO_TO_LOGIN_TEXT)


async def cancel_registration_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id')
    if user_id:
        response_text = cancel_registration(user_id)
        await update.message.reply_text(text=response_text, reply_markup=start_keyboard)
    else:
        await update.message.reply_text(text=GO_TO_LOGIN_TEXT)


async def check_my_registration_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id')
    if user_id:
        registration = check_registration(user_id)
        if registration is not None:
            await update.message.reply_text(
                text=registration,
                reply_markup=cancel_registration_keyboard
            )
        else:
            await update.message.reply_text(
                text='Вы не зарегистрированы ни на одну встречу',
                reply_markup=start_keyboard
            )
    else:
        await update.message.reply_text(text=GO_TO_LOGIN_TEXT)


async def get_qr_code_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id')
    if user_id:
        registration = get_current_registration(user_id)
        if registration is not None:
            file_path = generate_qr_code(registration)
            with open(file_path, 'rb') as qr_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=qr_file
                )
            os.remove(file_path)
        else:
            await update.message.reply_text(
                text='Вы не зарегистрированы ни на одну встречу',
                reply_markup=start_keyboard
            )
    else:
        await update.message.reply_text(text=GO_TO_LOGIN_TEXT)


def generate_random_filename(length=30):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_qr_code(info):
    qr = qrcode.QRCode(version=1, box_size=10, border=3)
    qr.add_data(info)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color='black', back_color='white')
    file_path = os.path.join(generate_random_filename() + '.png')
    qr_img.save(file_path)
    return file_path


def read_qr_code(image_path):
    image = Image.open(image_path)
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        decoded_data = barcode.data.decode('utf-8')
        return decoded_data
    return None
