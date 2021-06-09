from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.admin.callbacks import make_menu_callback
from loader import _


def get_admin_menu():
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row(InlineKeyboardButton(text=_("Заказы"), callback_data=make_menu_callback(table="Order", level=1)))
    return markup


def get_menu_buttons(table, level_back=0, only_back=False):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    if only_back is False:
        markup.row(InlineKeyboardButton(text=_("Посмотреть записи 📖"), callback_data=make_menu_callback(
            table=table,
            action="show",
            level=2
        )))
        markup.row(InlineKeyboardButton(text=_("Найти запись 🔎"), callback_data=make_menu_callback(
            table=table,
            action="find",
            level=2)))
    markup.row(InlineKeyboardButton(text=_("Назад ↩️"), callback_data=make_menu_callback(
        table=table,
        level=level_back)))
    return markup
