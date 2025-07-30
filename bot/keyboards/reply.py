from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    kb = [
        [KeyboardButton(text="Оставить заявку")],
        [KeyboardButton(text="О нас")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_confirm_keyboard():
    kb = [
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)