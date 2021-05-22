from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                    keyboard=[
                                        [
                                            KeyboardButton(text=_("🗂Каталог")),
                                            KeyboardButton(text=_("🛒Корзина"))
                                        ],
                                        [
                                            KeyboardButton(text=_("📦Мои заказы")),
                                            KeyboardButton(text=_("❓Помощь"))
                                        ],
                                        [
                                            KeyboardButton(text=_("Изменить язык"))
                                        ]
                                    ]
                                    )
