from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove

REGISTER = 'Зарегистрироваться'
RETURN = 'Вернуться'
STEP_REGISTER_CALLBACK = 'steps_register'
BAPTISM_REGISTER_CALLBACK = 'baptism_register'
RETURN_CALLBACK = 'return'

start_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text=REGISTER), KeyboardButton(text='Мои регистрации')],
], resize_keyboard=True, one_time_keyboard=True)

select_meeting_type_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text='Первые шаги'), KeyboardButton(text='Крещение')],
    [KeyboardButton(text=RETURN)]
], resize_keyboard=True, one_time_keyboard=True)

select_first_step_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text='Записаться на шаги')],
    [KeyboardButton(text=RETURN)]
], resize_keyboard=True, one_time_keyboard=True)

register_to_meeting_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text=REGISTER, callback_data=STEP_REGISTER_CALLBACK)],
    [InlineKeyboardButton(text=RETURN, callback_data=RETURN_CALLBACK)]
])

cancel_registration_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text='Отменить регистрацию'), KeyboardButton(text='Получить QR код')],
    [KeyboardButton(text=RETURN)]
], resize_keyboard=True, one_time_keyboard=True)

sign_up_for_baptism_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='Записаться на крещение', callback_data=BAPTISM_REGISTER_CALLBACK)],
     [InlineKeyboardButton(text=RETURN, callback_data=RETURN_CALLBACK)]
])

remove_keyboard = ReplyKeyboardRemove()
