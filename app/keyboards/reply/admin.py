from app.keyboards.reply.base import *


def admin_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.admin.statistic), KeyboardButton(Buttons.admin.rating)],
            [KeyboardButton(Buttons.admin.delete), KeyboardButton(Buttons.admin.update)],
            [KeyboardButton(Buttons.menu.main_menu[lang])]
        ]
    )


def update_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.admin.phones)],
            [KeyboardButton(Buttons.admin.names)],
            [KeyboardButton(Buttons.admin.back)]
        ]
    )


def delete_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton('Так')],
            [KeyboardButton('Відмінити')]
        ]
    )