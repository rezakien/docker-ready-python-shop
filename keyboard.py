from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard(type_keyboard='language'):
    if type_keyboard == 'language':
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="O'zbekcha"),
                    KeyboardButton(text="Русский")
                ],
                [
                    KeyboardButton(text="Отмена"),
                ]
            ]
        )
    if type_keyboard == 'poll':
        poll_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        poll_keyboard.add(KeyboardButton(text="Корзина"))
        poll_keyboard.add(KeyboardButton(text="Отмена"))
        return poll_keyboard
    if type_keyboard == 'default':
        poll_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        poll_keyboard.add(KeyboardButton(text="Корзина"))
        poll_keyboard.add(KeyboardButton(text="Отмена"))
    if not type_keyboard:
        return ReplyKeyboardRemove()
