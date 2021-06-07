from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from loader import dp, _, get_all_language_variants
from utils.db.models import Order
from utils.helpers.decorators import user_sign_in_message


@dp.message_handler(Text(equals=get_all_language_variants("Заказы 📦")))
@user_sign_in_message
async def menu_orders_handler(message: Message):
    text = ""
    reply_markup = None
    all_items = await Order.get_orders()
    if len(all_items) == 0:
        text = _("У вас пока нет заказов.")
    await message.answer(text=text, reply_markup=reply_markup)
