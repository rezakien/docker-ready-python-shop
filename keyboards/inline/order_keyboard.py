from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbacks import order_callback
from loader import _


def get_order_keyboard(order_id, canceled=False):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row(
        InlineKeyboardButton(
            text=_("Посмотреть товары 🔎"),
            callback_data=order_callback.new(order_id=order_id, action="show_items")
        )
    )
    if canceled is not True:
        markup.row(
            InlineKeyboardButton(
                text=_("Отменить заказ ❌"),
                callback_data=order_callback.new(order_id=order_id, action="cancel_order")
            )
        )
    return markup
