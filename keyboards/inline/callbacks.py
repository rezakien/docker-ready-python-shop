from aiogram.utils.callback_data import CallbackData

language_callback = CallbackData("language_callback", "lang")
category_callback = CallbackData("category_callback", "category", "show_items", "item_id")
item_callback = CallbackData("item_callback", "item_id", "quantity", "place")
cart_callback = CallbackData("cart_callback", "action")
order_callback = CallbackData("order_callback", "order_id", "action", "admin")


def make_callback_data(category="0", show_items="False", item_id="0"):
    return category_callback.new(category=category, show_items=show_items, item_id=item_id)
