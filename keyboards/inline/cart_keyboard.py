from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbacks import cart_callback
from loader import _


def get_cart_keyboard():
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row(InlineKeyboardButton(text=_("Очистить 🛒"), callback_data=cart_callback.new(action="clear_cart")))
    markup.row(InlineKeyboardButton(text=_("Посмотреть товары"), callback_data=cart_callback.new(action="show_cart_items")))
    return markup
