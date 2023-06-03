from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove

REGISTER = 'Зарегистрироваться'
REGISTER_CALLBACK = 'register'

start_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text=REGISTER), KeyboardButton(text='Мои регистрации')],
], resize_keyboard=True, one_time_keyboard=True)

register_to_meeting_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text=REGISTER, callback_data=REGISTER_CALLBACK)]
])

remove_keyboard = ReplyKeyboardRemove()

cancel_registration_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text='Отменить регистрацию'), KeyboardButton(text='Получить QR код')],
    [KeyboardButton(text='Вернуться')]
], resize_keyboard=True)
