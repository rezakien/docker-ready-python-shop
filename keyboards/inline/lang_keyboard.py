from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbacks import language_callback


def get_lang_keyboard():
    return InlineKeyboardMarkup(resize_keyboard=True,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text="Русский 🇷🇺",
                                                          callback_data=language_callback.new(lang="ru"))],
                                    [InlineKeyboardButton(text="O'zbekcha 🇺🇿",
                                                          callback_data=language_callback.new(lang="uz"))]
                                ])
