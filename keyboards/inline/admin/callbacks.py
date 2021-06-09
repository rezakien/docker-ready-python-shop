from aiogram.utils.callback_data import CallbackData

menu_callback = CallbackData("menu_callback", "table", "action", "level")


def make_menu_callback(table="-", action="-", level="-"):
    return menu_callback.new(table, action, level)
