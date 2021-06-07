from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_contacts_keyboard(locale=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(_("Оформить заказ ✅", locale=locale)),
        ],
        [
            KeyboardButton(_("Назад ⬅️", locale=locale))
        ],
    ])
    return markup


def get_contact_keyboard(locale=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(_("Контакт 📞", locale=locale), request_contact=True),
        ],
    ])
    return markup


def get_location_keyboard(locale=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(_("Локация 📍", locale=locale), request_location=True),
        ],
    ])
    return markup
