import logging
import asyncio
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
import config
from language_middleware import setup_middleware

# logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
#                     level=logging.INFO,
#                     )

loop = asyncio.get_event_loop()

storage = MemoryStorage()


bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

i18n = setup_middleware(dp)
_ = i18n.gettext


def get_all_language_variants(i18n_word) -> List:
    return [_(i18n_word, locale=locale) for locale in ['uz', 'ru']]
