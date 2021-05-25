from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from constants.lang import LANGUAGES
from keyboards.inline.callbacks import language_callback

languages = LANGUAGES


def get_lang_keyboard():
    return InlineKeyboardMarkup(resize_keyboard=True,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text=language["title"],
                                                          callback_data=language_callback.new(lang=language["prefix"]))
                                     for language in languages]
                                ])
