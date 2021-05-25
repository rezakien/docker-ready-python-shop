from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    Location = State()
    Contact = State()
