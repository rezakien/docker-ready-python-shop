from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callbacks import lang_callback

lang_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text="Русский", callback_data=lang_callback.new(lang="ru")),
                                             InlineKeyboardButton(text="O'zbekcha", callback_data=lang_callback.new(lang="uz")),
                                         ]
                                     ]
                                 )
