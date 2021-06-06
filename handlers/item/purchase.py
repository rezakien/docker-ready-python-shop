from aiogram.types import CallbackQuery

from keyboards.inline.callbacks import item_callback
from keyboards.inline.cart_keyboard import get_cart_item_text
from keyboards.inline.menu_keyboard import item_keyboard
from loader import dp, _
from utils.db import Item, Cart, User
from utils.helpers.decorators import user_sign_in_callback


@dp.callback_query_handler(item_callback.filter())
@user_sign_in_callback
async def item_cart_resolve(call: CallbackQuery, callback_data: dict):
    get_current = call.message.from_user.get_current()
    user = await User.get_user(get_current["id"])

    item_id = int(callback_data.get("item_id"))
    quantity = int(callback_data.get("quantity"))
    place = callback_data.get("place")
    item = await Item.get_item(item_id)
    text = ""
    res = await Cart.create_update_item(item_id=item.id, user_id=user.id, quantity=quantity)
    if res:
        if quantity > 0:
            text = _("Добавлено {quantity} шт. {item_name}".format(quantity=quantity, item_name=item.name))
            if place == 'cart':
                cart_item = await Cart.get_cart_item(item_id)
                if cart_item:
                    text_in_cart = await get_cart_item_text(cart_item, item)
                    reply_markup = item_keyboard(item.id, 'cart')
                    await call.message.edit_text(text=text_in_cart, reply_markup=reply_markup)
        if quantity == 0:
            text = _("Товар удален из корзины".format(item.name))
            if place == 'cart':
                await call.message.edit_text(text=_("Товар {item_name} удален из корзины".format(item_name=item.name)))
                await call.message.edit_reply_markup()
    await call.answer(text=text, cache_time=1)
