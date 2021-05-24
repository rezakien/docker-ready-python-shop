from aiogram.utils.callback_data import CallbackData

lang_callback = CallbackData("menu_lang", "lang")
category_callback = CallbackData("show_category", "category", "show_items", "item_id")
item_callback = CallbackData("buy_item", "item_id")


def make_callback_data(category="0", show_items="False", item_id="0"):
    return category_callback.new(category=category, show_items=show_items, item_id=item_id)
