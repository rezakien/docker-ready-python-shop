from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callbacks import order_callback
from loader import _


def get_order_text_and_keyboard_admin(order):
    status = _("Завершен ✅") if order.successful == True else _("Обрабатывается 🕗")
    if order.canceled is True:
        status = _("Отменен ❌")
    order_text = _("Заказ №{order_id}\n"
                   "Сумма: {order_sum:,} сум.\n"
                   "Время оформления: {order_time}\n\n"
                   "Статус: {status}".format(order_id=order.id,
                                             order_sum=order.sum,
                                             order_time=order.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
                                             status=status))
    reply_markup = get_order_keyboard_admin(order.id, order.canceled)
    return {
        "order_text": order_text,
        "reply_markup": reply_markup
    }


def get_order_keyboard_admin(order_id, canceled=False):
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
                text=_("Завершить заказ ✅"),
                callback_data=order_callback.new(order_id=order_id, action="confirm_order")
            )
        )
        markup.row(
            InlineKeyboardButton(
                text=_("Отменить заказ ❌"),
                callback_data=order_callback.new(order_id=order_id, action="cancel_order")
            )
        )
    return markup