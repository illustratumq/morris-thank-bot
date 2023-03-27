from app.states.base import *


class AuthSG(StatesGroup):
    Lang = State()
    AuthData = State()


class SendSG(StatesGroup):
    Command = State()
    User = State()
    Message = State()
    Points = State()
    Value = State()
    CustomValue = State()
    Confirm = State()


class DeleteSG(StatesGroup):
    User = State()
    Confirm = State()
