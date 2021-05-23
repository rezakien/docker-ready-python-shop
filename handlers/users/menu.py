import asyncio
import logging
from typing import Union

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.default import menu_keyboard
from keyboards.inline.callbacks import lang_callback
from keyboards.inline.lang_keyboard import lang_keyboard
from loader import dp, _
from utils.db_api.database import DBCommands

db = DBCommands()


@dp.message_handler(Text(equals=[_("Каталог"), _("Корзина"), _("Мои заказы"), _("Помощь"), _("Изменить язык")]))
async def menu_handler(message: Message):
    menu_category = message.text
    text = ""
    if menu_category == _("Каталог"):
        text = _("Выберите категорию👇🏻")
        await message.answer(f"{text}", reply_markup=ReplyKeyboardRemove())
    if menu_category == _("Корзина"):
        text = _("У вас пока нет товаров в корзине.")
        await message.answer(f"{text}", reply_markup=ReplyKeyboardRemove())
    if menu_category == _("Мои заказы"):
        text = _("У вас пока нет заказов.")
        await message.answer(f"{text}", reply_markup=ReplyKeyboardRemove())
    if menu_category == _("Помощь"):
        text = _("Здесь вы можете получить информацию о боте.")
        await message.answer(f"{text}", reply_markup=ReplyKeyboardRemove())
    if menu_category == _("Изменить язык"):
        text = _("Выберите язык")
        await message.answer(f"{text}", reply_markup=lang_keyboard)


@dp.callback_query_handler(lang_callback.filter())
async def lang_handler(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    await db.set_language(lang)
    lang_text = 'русский язык.'
    if lang == 'uz':
        lang_text = "O'zbek"
    text = _("Вы выбрали {lang}".format(lang=lang_text), locale=lang)
    await call.message.edit_reply_markup()
    await call.message.answer(text, reply_markup=menu_keyboard)
