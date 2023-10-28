from aiogram.dispatcher.filters.state import StatesGroup, State


class NewPost(StatesGroup):
    fullName = State()  # ism
    phoneNum = State()  # Tel raqami
    NewMessage = State()# Xabar
    Confirm = State()
