from aiogram.types import CallbackQuery

from keyboards.inline.callbacks import item_callback
from loader import dp, _
from utils.db import Item, Cart, User


@dp.callback_query_handler(item_callback.filter())
async def item_cart_resolve(call: CallbackQuery, callback_data: dict):
    get_current = call.message.from_user.get_current()
    user = await User.get_user(get_current["id"])

    item_id = int(callback_data.get("item_id"))
    quantity = int(callback_data.get("quantity"))
    item = await Item.get_item(item_id)
    text = ""
    res = await Cart.create_update_item(item_id=item.id, user_id=user.id, quantity=quantity)
    if res:
        if quantity > 0:
            text = _("Добавлено {quantity} шт. {item_name}".format(quantity=quantity, item_name=item.name))
        if quantity == 0:
            text = _("Товар удален из корзины".format(item.name))
    await call.answer(text=text, cache_time=1)
