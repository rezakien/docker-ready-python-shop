from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbacks import order_callback
from loader import _


def get_order_keyboard(order):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row(
        InlineKeyboardButton(
            text=_("Посмотреть товары 🔎"),
            callback_data=order_callback.new(order_id=order.id, action="show_items", admin=False)
        )
    )
    if order.canceled is not True and order.successful is not True:
        markup.row(
            InlineKeyboardButton(
                text=_("Отменить заказ ❌"),
                callback_data=order_callback.new(order_id=order.id, action="cancel_order", admin=False)
            )
        )
    return markup


def get_order_text_and_keyboard(order):
    status = _("Завершен ✅") if order.successful == True else _("Обрабатывается 🕗")
    if order.canceled is True:
        status = _("Отменен ❌")
    order_text = _("<b>Заказ №{order_id}</b>\n"
                   "<b>Сумма:</b> {order_sum:,} сум.\n"
                   "<b>Время оформления:</b> {order_time}\n\n"
                   "<b>Статус:</b> {status}".format(order_id=order.id,
                                                    order_sum=order.sum,
                                                    order_time=order.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
                                                    status=status))
    reply_markup = get_order_keyboard(order)
    return {
        "order_text": order_text,
        "reply_markup": reply_markup
    }
