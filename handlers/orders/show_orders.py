from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callbacks import order_callback
from keyboards.inline.cart_keyboard import get_text
from keyboards.inline.order_keyboard import get_order_text_and_keyboard
from loader import dp, _, get_all_language_variants
from utils.db.models import Order, Item
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
            for order_item in order_items:
                item = await Item.get_item(order_item.item_id)
                photo = await item.get_photo()
                text = get_text(item.name, order_item.price, order_item.quantity)
                await call.message.answer_photo(photo=photo, caption=text)
    elif action == "cancel_order":
        order = await Order.cancel_order(order_id)
        res = get_order_text_and_keyboard(order)
        await call.message.edit_text(text=res.get("order_text"), reply_markup=res.get("reply_markup"))
    elif action == "confirm_order":
        order = await Order.confirm_order(order_id)
        res = get_order_text_and_keyboard(order)
        await call.message.edit_text(text=res.get("order_text"), reply_markup=res.get("reply_markup"))



