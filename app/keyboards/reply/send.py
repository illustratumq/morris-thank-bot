from app.database.models.user import User
from app.database.services.repos import PointRepo
from app.keyboards.reply.base import *


def send_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.send.select_user[lang])],
            [KeyboardButton(Buttons.menu.main_menu[lang])]
        ]
    )


def confirm_send_kb(lang):
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.send.confirm[lang])],
            [KeyboardButton(Buttons.menu.main_menu[lang])]
        ]
    )


def select_user_commands(commands: list, lang: str):
    keyboard = []
    cache = []
    i = 0
    for command in commands:
        cache.append(KeyboardButton(command))
        i += 1
        if i == 2:
            keyboard.append(cache)
            cache = []
            i = 0
    if len(cache) > 0:
        keyboard.append(cache)
    keyboard.append([KeyboardButton(Buttons.menu.main_menu[lang])])
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=keyboard
    )


async def select_user_kb(users: list[User], me: str, lang: str, admin: bool = False):
    keyboard = []
    cache = []
    i = 0
    for user in users:
        if user and user.full_name != me:
            cache.append(KeyboardButton(user.full_name))
            i += 1
            if i == 2:
                keyboard.append(cache)
                cache = []
                i = 0
    if len(cache) > 0:
        keyboard.append(cache)
    keyboard.append([KeyboardButton(Buttons.send.select_user[lang]),
                     KeyboardButton(Buttons.menu.main_menu[lang] if not admin else Buttons.admin.back)])
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=keyboard
    )


def values_kb(lang: str, next_button: bool = False, added_values: list[str] = None):
    keyboard = []
    cache = []
    i = 0
    values: list = Buttons.send.values(lang)
    if added_values:
        for val in added_values:
            if val in values:
                values.remove(val)
    for value in values:
        cache.append(KeyboardButton(value))
        i += 1
        if i == 2:
            keyboard.append(cache)
            cache = []
            i = 0
    if len(cache) > 0:
        keyboard.append(cache)
    if next_button:
        keyboard.append(
            [KeyboardButton(Buttons.send.custom_value[lang]), KeyboardButton(Buttons.send.next_button[lang])]
        )
    else:
        keyboard += [[KeyboardButton(Buttons.send.custom_value[lang])]]
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=keyboard
    )