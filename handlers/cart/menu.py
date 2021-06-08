import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType

from handlers.users.start import bot_start
from keyboards.default import get_contacts_keyboard, get_menu_keyboard
from keyboards.default.contacts_keyboard import get_location_keyboard, get_contact_keyboard
from keyboards.inline.callbacks import cart_callback
from keyboards.inline.cart_keyboard import get_cart_keyboard, get_items_with_keyboard
from loader import dp, _, get_all_language_variants, geo_loc
from states.order import OrderState
from utils.db.models import Cart, Order, OrderItem, User, Item
from utils.helpers.decorators import user_sign_in_message, user_sign_in_callback, user_sign_in_message_state
from decimal import Decimal


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
async def menu_cart_order_handler(message: Message):
    text = _("Пожалуйста, отправьте свою локацию")
    reply_markup = get_location_keyboard()
    await message.answer(text, reply_markup=reply_markup)
    await OrderState.Location.set()


@dp.message_handler(content_types=ContentType.LOCATION, state=OrderState.Location)
@user_sign_in_message_state
async def menu_cart_location_handler(message: ContentType.LOCATION, state: FSMContext):
    async with state.proxy() as data:
        data["location"] = message.location
    if message is not None:
        logging.info("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
    text = _("Пожалуйста, отправьте свой контакт")
    reply_markup = get_contact_keyboard()
    await message.answer(text, reply_markup=reply_markup)
    await OrderState.Contact.set()


@dp.message_handler(content_types=ContentType.CONTACT, state=OrderState.Contact)
@user_sign_in_message_state
async def menu_cart_contact_handler(message: ContentType.LOCATION, state: FSMContext):
    async with state.proxy() as data:
        data["contact"] = message.contact
    res = await save_order(state)
    if res:
        text = _("Заказ подтвержден! Ждите звонка, либо сообщения от нашего оператора.")
    else:
        text = _("Что-то пошло не так, повторите попытку.")
    reply_markup = get_menu_keyboard()
    await state.reset_state()
    await message.answer(text, reply_markup=reply_markup)


async def save_order(state: FSMContext):
    async with state.proxy() as data:
        location = data.get("location")
        contact = data.get("contact")
        if location is not None and contact is not None:
            summary = await Cart.get_cart_sum()
            if summary > 0:
                current = types.User.get_current()
                user = await User.get_user(current.id)
                latitude = location.latitude
                longitude = location.longitude
                address = geo_loc.reverse("{}, {}".format(latitude, longitude), language='uz').address
                order = await Order(user_id=user.id,
                                    phone_number=contact["phone_number"],
                                    latitude=latitude,
                                    longitude=longitude,
                                    address=address if address is not None and address != '' else None,
                                    sum=summary).create()
                cart_items = await Cart.get_cart_items()
                for cart_item in cart_items:
                    item = await Item.get_item(cart_item.item_id)
                    price = await item.get_price(cart_item.quantity)
                    quantity = cart_item.quantity
                    summary = price * quantity
                    order_item = await OrderItem(
                        order_id=order.id,
                        item_id=item.id,
                        price=price,
                        quantity=quantity,
                        user_id=user.id,
                        summary=summary
                    ).create()
                await Cart.clear_cart()
                return True
            else:
                return False
