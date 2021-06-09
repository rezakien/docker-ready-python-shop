from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callbacks import order_callback
from loader import _


def get_order_text_and_keyboard_admin(order):
    status = _("Завершен ✅") if order.successful == True else _("Обрабатывается 🕗")
    if order.canceled is True:
        status = _("Отменен ❌")
    phone_number = "<a href='tel:{}'>{}</a>".format(order.phone_number, order.phone_number)
    order_text = _("<b>Заказ №{order_id}</b>\n"
                   "<b>Сумма:</b> {order_sum:,} сум.\n\n"
                   "<b>Номер телефона:</b> {phone_number}\n"
                   "<b>Адрес доставки:</b> {address}\n\n"
                   "<b>Время оформления:</b> {order_time}\n"
                   "<b>Статус:</b> {status}".format(order_id=order.id,
                                                    order_sum=order.sum,
                                                    order_time=order.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
                                                    status=status,
                                                    phone_number=phone_number,
                                                    address=order.address
                                                    )
                   )
    reply_markup = get_order_keyboard_admin(order)
    return {
        "order_text": order_text,
        "reply_markup": reply_markup
    }


def get_order_keyboard_admin(order):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row(
        InlineKeyboardButton(
            text=_("Посмотреть товары 🔎"),
            callback_data=order_callback.new(order_id=order.id, action="show_items", admin=True)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_("Посмотреть адрес 📍"),
            callback_data=order_callback.new(order_id=order.id, action="show_address", admin=True)
        )
    )
    if order.canceled is not True and order.successful is not True:
        markup.row(
            InlineKeyboardButton(
                text=_("Завершить заказ ✅"),
                callback_data=order_callback.new(order_id=order.id, action="confirm_order", admin=True)
            )
        )
        markup.row(
            InlineKeyboardButton(
                text=_("Отменить заказ ❌"),
                callback_data=order_callback.new(order_id=order.id, action="cancel_order", admin=True)
            )
        )
    return markup
