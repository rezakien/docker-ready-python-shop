from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from handlers.users.start import bot_start
from keyboards.default import get_contacts_keyboard, get_menu_keyboard
from keyboards.inline.callbacks import cart_callback
from keyboards.inline.cart_keyboard import get_cart_keyboard, get_items_with_keyboard
from loader import dp, _, get_all_language_variants
from utils.db.models import Cart
from utils.helpers.decorators import user_sign_in_message, user_sign_in_callback


def get_word_items(count):
    if count % 10 == 2:
        return _('товара')
    elif count % 10 == 1:
        return _('товар')
    else:
        return _('товаров')


@dp.message_handler(Text(equals=get_all_language_variants("Корзина 🛒")))
@user_sign_in_message
async def menu_cart_handler(message: Message):
    text = ""
    reply_markup = None
    all_items = await Cart.get_cart()
    all_items_sum = await Cart.get_cart_sum()
    if len(all_items) == 0:
        text = _("У вас пока нет товаров в корзине.")
    else:
        text = _("В вашей корзине <b>{items_count} {items_word}</b>."
                 "\n<b>На сумму</b>: {sum:,} сум.").format(
            items_count=len(all_items),
            items_word=get_word_items(len(all_items)),
            sum=all_items_sum
        )
        reply_markup = get_cart_keyboard()
    await message.answer(text=text, reply_markup=reply_markup)


@dp.callback_query_handler(cart_callback.filter())
@user_sign_in_callback
async def cart_callback_handler(call: CallbackQuery, callback_data: dict):
    action = callback_data.get("action")
    text = ""
    reply_markup = None
    if action == 'clear':
        text = _("Корзина очищена")
        await Cart.clear_cart()
        await call.message.edit_reply_markup()
        await call.message.edit_text(text=text)
    if action == 'show':
        text = _("Просмотр товаров в корзине")
        await call.message.edit_text(text=text)
        await get_items_with_keyboard(call)
    if action == 'order':
        text = _("Вы уверены, что хотите оформить заказ?")
        reply_markup = get_contacts_keyboard()
        await call.message.edit_reply_markup()
        await call.message.answer(text=text, reply_markup=reply_markup)


@dp.message_handler(Text(equals=get_all_language_variants("Назад ⬅️")))
@user_sign_in_message
async def menu_cart_back_handler(message: Message):
    await menu_cart_handler(message=message)
    await bot_start(message)


@dp.message_handler(Text(equals=get_all_language_variants("Оформить заказ ✅")))
@user_sign_in_message
async def menu_cart_back_handler(message: Message):
    pass