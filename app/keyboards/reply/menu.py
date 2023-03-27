from app.keyboards.reply.base import *


def menu_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                KeyboardButton(Buttons.menu.send_points[lang]), KeyboardButton(Buttons.menu.my_profile[lang]),
            ],
            [
                KeyboardButton(Buttons.menu.rules[lang]), KeyboardButton(Buttons.menu.history[lang])
            ],
            [
                KeyboardButton(Buttons.menu.info[lang])
            ]
        ]
    )


def to_menu_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(text)] for text in Buttons.menu.go_next[lang]
        ]
    )


def main_menu_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.menu.main_menu[lang])]
        ]
    )


def my_profile_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.menu.history[lang])],
            [KeyboardButton(Buttons.menu.main_menu[lang])]
        ]
    )


def pre_history_kb(lang: str):
    return  ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.menu.my_send[lang]), KeyboardButton(Buttons.menu.to_me_send[lang])],
            [KeyboardButton(Buttons.menu.main_menu[lang])]
        ]
    )


def back_to_history_kb(lang: str):
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.menu.back_to_history[lang])]
        ]
    )


def to_auth(lang: str):
    return ReplyKeyboardMarkup(
        row_width=1,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [KeyboardButton(Buttons.menu.auth_bt[lang])]
        ]
    )