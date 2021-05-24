from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbacks import make_callback_data, item_callback
from utils.db_api import Category


async def get_categories_keyboard():
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    categories = await Category.all_parents()
    for category in categories:
        callback_data = make_callback_data(category=category.id)
        markup.insert(
            InlineKeyboardButton(text=category.name, callback_data=callback_data)
        )
    return markup


async def get_subcategories_keyboard(category_id):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)

    current_category_items_count = await Category.count_items(category_id)
    sub_categories = await Category.all_subcategories_of_category(category_id)

    for sub_category in sub_categories:
        sub_category_sub_categories = await Category.all_subcategories_of_category(sub_category.id)
        show_items = False
        if len(sub_category_sub_categories) == 0:
            show_items = True
        items_count = await Category.count_items(sub_category.id)
        callback_data = make_callback_data(category=sub_category.id, show_items=show_items)

        text = f"{sub_category.name} ({items_count} шт.)"
        markup.insert(
            InlineKeyboardButton(text=text, callback_data=callback_data)
        )

    if current_category_items_count > 0 and len(sub_categories) > 0:
        markup.row(
            InlineKeyboardButton(
                text=f"Посмотреть товары {current_category_items_count} шт.",
                callback_data=make_callback_data(category=category_id, show_items=True)
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(category=category_id)
        )
    )
    return markup


async def get_items_keyboard(category):
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    items = await Category.all_items_of_category(category)
    if len(items) > 0:

        for item in items:
            callback_data = make_callback_data(category=category,
                                               item_id=item.id)
            button_text = f"{item.name} - {item.price} сум."
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=callback_data)
            )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(category=category)
        )
    )
    return markup


def item_keyboard(category, item_id):
    inline_keyboard = [InlineKeyboardButton(
        text="+25",
        callback_data=item_callback.new(item_id=item_id)
    ), InlineKeyboardButton(
        text="+100",
        callback_data=item_callback.new(item_id=item_id)
    ), InlineKeyboardButton(
        text="+500",
        callback_data=item_callback.new(item_id=item_id)
    ), InlineKeyboardButton(
        text="🗑",
        callback_data=item_callback.new(item_id=item_id)
    )]
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.row(*inline_keyboard)
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(category=category)
        ),
    )
    return markup
