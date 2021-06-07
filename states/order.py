from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderState(StatesGroup):
    Location = State()
    Contact = State()
