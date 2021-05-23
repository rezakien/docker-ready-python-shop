from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(_("Каталог")),
        KeyboardButton(_("Корзина"))
    ],
    [
        KeyboardButton(_("Мои заказы")),
        KeyboardButton(_("Помощь"))
    ],
    [
        KeyboardButton(_("Изменить язык"))
    ]
]
                                )
