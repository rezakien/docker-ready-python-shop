from aiogram.types import CallbackQuery

from keyboards.inline.callbacks import item_callback
from keyboards.inline.cart_keyboard import get_cart_item_text
from keyboards.inline.menu_keyboard import item_keyboard
from loader import dp, _
from utils.db.models import Cart, Item, User
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
    if res["success"] is True:
        if quantity > 0:
            cart_item = await Cart.get_cart_item(item.id)
            item_price = await item.get_price(cart_item.quantity)
            text = _("Добавлено {quantity} кг. {item_name} по {item_price:,} сум.".format(quantity=quantity, item_name=item.name, item_price=item_price))
        if quantity == 0:
            text = _("Товар удален из корзины".format(item.name))
        await reply_item(quantity, place, item, call)
    else:
        if res["message"] == "ERROR_CAPACITY":
            text = _("Минимальный объем товара составляет 100 кг.")
        elif res["message"] == "UNKNOWN_ERROR":
            text = _("Произошла неизвестная ошибка при удалении.")
    await call.answer(text=text, cache_time=1)


async def reply_item(quantity, place, item, call):
    if place == 'category':
        text = await item.get_item_text()
        reply_markup = item_keyboard(item.id)
        await call.message.edit_caption(caption=text, reply_markup=reply_markup)
    if place == 'cart':
        if quantity > 0:
            cart_item = await Cart.get_cart_item(item.id)
            if cart_item:
                text_in_cart = await get_cart_item_text(cart_item, item)
                reply_markup = item_keyboard(item.id, 'cart')
                await call.message.edit_text(text=text_in_cart, reply_markup=reply_markup)
        if quantity == 0:
            text = _("Товар удален из корзины".format(item.name))
            if place == 'cart':
                await call.message.edit_text(text=_("Товар {item_name} удален из корзины".format(item_name=item.name)))
                await call.message.edit_reply_markup()


