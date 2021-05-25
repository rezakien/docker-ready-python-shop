from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callbacks import cart_callback
from keyboards.inline.cart_keyboard import get_cart_keyboard
from loader import dp, _, get_all_language_variants
from utils.db import Cart


@dp.message_handler(Text(equals=get_all_language_variants("Корзина 🛒")))
async def menu_cart_handler(message: Message):
    text = ""
    reply_markup = None
    all_items = await Cart.get_cart()
    all_items_sum = await Cart.get_cart_sum()
    if len(all_items) == 0:
        text = _("У вас пока нет товаров в корзине. ")
    else:
        text = _("В вашей корзине <b>{items_count} {items_word}</b>."
                 "\n<b>На сумму</b>: {sum:,} сум.").format(
            items_count=len(all_items),
            items_word=get_word_items(len(all_items)),
            sum=all_items_sum
        )
        reply_markup = get_cart_keyboard()
    await message.answer(f"{text}", reply_markup=reply_markup)


@dp.callback_query_handler(cart_callback.filter())
async def cart_callback_handler(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    action = callback_data.get("action")
    text = ""
    reply_markup = None
    if action == 'clear_cart':
        await Cart.clear_cart()
        text = _("Корзина очищена")
        await call.message.edit_text(text=text)


def get_word_items(count):
    if count % 10 == 2:
        return _('товара')
    elif count % 10 == 1:
        return _('товар')
    else:
        return _('товаров')

