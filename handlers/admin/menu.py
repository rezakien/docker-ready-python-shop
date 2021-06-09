import logging

from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.admin.menu import get_menu_buttons, get_admin_menu
from keyboards.inline.admin.order import get_order_text_and_keyboard_admin
from loader import dp, _
from keyboards.inline.admin.callbacks import menu_callback
from utils.helpers.decorators import admin_sign_in_callback
from utils.db import models


@dp.callback_query_handler(menu_callback.filter())
@admin_sign_in_callback
async def orders(call: CallbackQuery, callback_data: dict):
    table = callback_data.get("table")
    action = callback_data.get("action")

    level = callback_data.get("level")

    levels = {
        "0": get_menu,
        "1": get_sub_menu,
        "2": call_action
    }

    current_level_function = levels[level]
    await current_level_function(call, table=table, action=action)


async def get_menu(callback: CallbackQuery, **kwargs):
    markup = get_admin_menu()
    text = _("Выберите, что хотите посмотреть/редактировать.")
    await callback.message.edit_text(text=text)
    await callback.message.edit_reply_markup(markup)


async def get_sub_menu(callback: CallbackQuery, table, **kwargs):
    markup = get_menu_buttons(table)
    text = _("Выберите действие.")
    await callback.message.edit_text(text=text)
    await callback.message.edit_reply_markup(reply_markup=markup)


async def call_action(callback: CallbackQuery, table, action, **kwargs):
    if action == "show":
        rows = await getattr(models, table).query.gino.all()
        await show_action(callback, table, rows)


async def show_action(callback: CallbackQuery, table, rows, **kwargs):
    if table == 'Order':
        for row in rows:
            res = get_order_text_and_keyboard_admin(row)
            await callback.message.answer(text=res.get("order_text"), reply_markup=res.get("reply_markup"))
    markup = get_menu_buttons(table=table, level_back=1, only_back=True)
    await callback.message.answer(text=_("Назад в меню заказов."), reply_markup=markup)