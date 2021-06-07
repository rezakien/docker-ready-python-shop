from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton

from keyboards.inline.callbacks import cart_callback
from keyboards.inline.menu_keyboard import item_keyboard
from loader import _
from utils.db import Cart, Item


def get_cart_keyboard():
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.row(InlineKeyboardButton(text=_("Очистить 🛒"), callback_data=cart_callback.new(action="clear")))
    markup.row(InlineKeyboardButton(text=_("Посмотреть товары 🔎"), callback_data=cart_callback.new(action="show")))
    markup.row(InlineKeyboardButton(text=_("К оформлению заказа ✅"), callback_data=cart_callback.new(action="order")))
    return markup


async def get_items_with_keyboard(call: CallbackQuery):
    cart_items = await Cart.get_cart_items()
    if len(cart_items) > 0:
        for cart_item in cart_items:
            item = await Item.get_item(cart_item.item_id)
            text = await get_cart_item_text(cart_item, item)
            reply_markup = item_keyboard(item.id, 'cart')
            await call.message.answer(text=text, reply_markup=reply_markup)


async def get_cart_item_text(cart_item, item):
    item = await Item.get_item(cart_item.item_id)
    price = await item.get_price(cart_item.quantity)
    return _("<b>Товар:</b> {item_name}\n"
             "<b>Цена за кг:</b> {price:,} сум.\n"
             "<b>Объем:</b> {quantity:,} кг.\n"
             "<b>Стоимость товара: </b> {summary:,} сум.".format(item_name=item.name, price=int(price),
                                                               quantity=cart_item.quantity,
                                                               summary=cart_item.quantity * int(price)))
