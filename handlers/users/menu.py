import logging

from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.inline.callbacks import lang_callback
from keyboards.inline.lang_keyboard import lang_keyboard
from loader import dp, _
from utils.db_api.database import DBCommands

db = DBCommands()


@dp.message_handler(Text(equals=[_("🗂Каталог"), _("🛒Корзина"), _("📦Мои заказы"), _("❓Помощь"), _("Изменить язык")]))
async def menu_handler(message: Message):
    menu_category = message.text
    text = ""
    reply_markup = None
    if menu_category == _('🗂Каталог'):
        text = _("Выберите категорию👇🏻")
        reply_markup = None
    if menu_category == _('🛒Корзина'):
        text = _("У вас пока нет товаров в корзине.")
        reply_markup = None
    if menu_category == _('📦Мои заказы'):
        text = _("У вас пока нет заказов.")
        reply_markup = None
    if menu_category == _('❓Помощь'):
        text = _("Здесь вы можете получить информацию о боте.")
        reply_markup = None
    if menu_category == _('Изменить язык'):
        text = _("Выберите язык")
        reply_markup = lang_keyboard
    await message.answer(f"{text}", reply_markup=reply_markup)


@dp.callback_query_handler(lang_callback.filter())
async def menu_handler(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    await call.answer(cache_time=60)
    lang = callback_data.get("lang")
    await db.set_language(lang)
    text = _("Вы выбрали {}".format(lang), locale='lang')
    await call.message.answer(text)
    await call.message.edit_reply_markup()
