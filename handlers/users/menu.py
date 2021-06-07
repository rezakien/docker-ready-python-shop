from pathlib import Path

from aiogram.types import Message, User
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.default import get_menu_keyboard

from keyboards.inline.callbacks import language_callback
from keyboards.inline.callbacks import category_callback

from keyboards.inline.lang_keyboard import get_lang_keyboard
from keyboards.inline.menu_keyboard import get_categories_keyboard, get_subcategories_keyboard, get_items_keyboard, \
    item_keyboard

from loader import dp, _, get_all_language_variants
from utils.db import Item
from utils.db.models.user import User
import logging

from utils.helpers.decorators import user_sign_in_message, user_sign_in_callback


@dp.message_handler(Text(equals=get_all_language_variants("Категории 🗂")))
async def menu_category_handler(message: Message):
    text = _("Выберите категорию 👇🏻")
    reply_markup = await get_categories_keyboard()
    await message.answer(f"{text}", reply_markup=reply_markup)


@dp.message_handler(Text(equals=get_all_language_variants("Помощь ❓")))
async def menu_help_handler(message: Message):
    text = _("Здесь вы можете получить информацию о боте.")
    reply_markup = None
    await message.answer(f"{text}", reply_markup=reply_markup)


@dp.message_handler(Text(equals=get_all_language_variants("Изменить язык 🌐")))
@user_sign_in_message
async def menu_language_handler(message: Message):
    text = _("Выберите язык:")
    reply_markup = get_lang_keyboard()
    await message.answer(f"{text}", reply_markup=reply_markup)


@dp.callback_query_handler(language_callback.filter())
@user_sign_in_callback
async def lang_handler(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    lang = callback_data.get("lang")
    await User.set_language(lang)
    text = _("Язык изменен.", locale=lang)
    await call.message.edit_reply_markup()
    await call.message.answer(text=text, reply_markup=get_menu_keyboard(lang))


@dp.callback_query_handler(category_callback.filter())
async def categories_handler(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    current_level = "0"
    category = int(callback_data.get("category"))
    item_id = int(callback_data.get("item_id"))
    show_items = callback_data.get("show_items")

    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
        "3": show_item,
    }
    if category == "0":
        current_level = "0"
    if category != "0":
        current_level = "1"
    if show_items == "True":
        current_level = "2"
    if item_id != 0:
        current_level = "3"
    current_level_function = levels[current_level]

    await current_level_function(call, category=category, item_id=item_id)


async def list_categories(callback: CallbackQuery, **kwargs):
    markup = await get_categories_keyboard()
    await callback.message.edit_reply_markup(markup)


async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await get_subcategories_keyboard(category)
    if len(markup.inline_keyboard) > 0:
        await callback.message.edit_text(text=_("Выберите подкатегорию 👇🏻"))
        await callback.message.edit_reply_markup(markup)
    else:
        await callback.message.edit_reply_markup()
        await callback.message.edit_text(text=_("По выбранной категории нет товаров и подкатегорий"))


async def list_items(callback: CallbackQuery, category, **kwargs):
    markup = await get_items_keyboard(category)
    await callback.message.edit_text(text=_("Выберите товар 👇🏻"))
    await callback.message.edit_reply_markup(reply_markup=markup)


async def show_item(callback: CallbackQuery, item_id, **kwargs):
    markup = item_keyboard(item_id)
    item = await Item.get_item(item_id)
    text = await item.get_item_text()
    text = f"{text}"

    photo = await item.get_photo()
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(text=_("Вы выбрали товар 👇🏻"))
    await callback.message.answer_photo(photo=photo, caption=text, reply_markup=markup)


