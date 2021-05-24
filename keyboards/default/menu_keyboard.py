from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_menu_keyboard(locale=None):
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(_("Категории 🗂", locale=locale)), KeyboardButton(_("Корзина 🛒", locale=locale))],
        [KeyboardButton(_("Заказы 📦", locale=locale)), KeyboardButton(_("Помощь ❓", locale=locale))],
        [KeyboardButton(_("Изменить язык 🌐", locale=locale))]
    ])


def get_admin_menu_keyboard(locale=None):
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(_("Категории 🗂", locale=locale)), KeyboardButton(_("Товары 🗂", locale=locale))],
        [KeyboardButton(_("Заказы 🗂", locale=locale)), KeyboardButton(_("Изменить язык 🌐", locale=locale))]
    ])
