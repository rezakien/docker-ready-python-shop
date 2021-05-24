from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from loader import dp, _, get_all_language_variants
from utils.db_api import Cart


@dp.message_handler(Text(equals=get_all_language_variants("Корзина 🛒")))
async def menu_cart_handler(message: Message):
    text = ""
    reply_markup = None
    all_items = await Cart.get_cart()
    if len(all_items) == 0:
        text = _("У вас пока нет товаров в корзине. ")
    else:
        text = "В вашей корзине {n} товаров.".format(n=len(all_items))
    await message.answer(f"{text}", reply_markup=reply_markup)