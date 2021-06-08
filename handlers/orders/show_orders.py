from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callbacks import order_callback
from keyboards.inline.cart_keyboard import get_cart_item_text, get_text
from keyboards.inline.order_keyboard import get_order_keyboard
from loader import dp, _, get_all_language_variants
from utils.db.models import Order, User, Cart, Item
from utils.helpers.decorators import user_sign_in_message, user_sign_in_callback


@dp.message_handler(Text(equals=get_all_language_variants("Заказы 📦")))
@user_sign_in_message
async def menu_orders_handler(message: Message):
    orders = await Order.get_orders()
    if len(orders) == 0:
        await message.answer(text=_("У вас пока нет заказов."))
    else:
        await message.answer(text=_("Ваши заказы 📦"))
        for index, order in enumerate(orders):
            res = get_order_text_and_keyboard(order)
            await message.answer(text=res.get("order_text"), reply_markup=res.get("reply_markup"))


@dp.callback_query_handler(order_callback.filter())
@user_sign_in_callback
async def order_callback_handler(call: CallbackQuery, callback_data: dict):
    order_id = int(callback_data.get("order_id"))
    action = callback_data.get("action")
    if action == "show_items":
        order_items = await Order.get_order_items(order_id)
        if len(order_items) > 0:
            await call.message.edit_reply_markup()
            await call.message.edit_text(text=_("Просмотр товаров заказа №{}".format(order_id)))
            for order_item in order_items:
                item = await Item.get_item(order_item.item_id)
                photo = await item.get_photo()
                text = get_text(item.name, order_item.price, order_item.quantity)
                await call.message.answer_photo(photo=photo, caption=text)
    elif action == "cancel_order":
        order = await Order.cancel_order(order_id)
        res = get_order_text_and_keyboard(order)
        await call.message.edit_text(text=res.get("order_text"), reply_markup=res.get("reply_markup"))


def get_order_text_and_keyboard(order):
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
    reply_markup = get_order_keyboard(order.id, order.canceled)
    return {
        "order_text": order_text,
        "reply_markup": reply_markup
    }
