from app.keyboards.inline.base import *
from app.keyboards.reply.base import *


lang_kb = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [KeyboardButton('Українська'), KeyboardButton('Російська')]
    ]
)


def auth_kb(auth_method: str, lang: str):
    if auth_method == 'Phone':
        return ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=False,
            keyboard=[
                [KeyboardButton(Buttons.menu.share_phone[lang], request_contact=True)]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=Buttons.menu.auth.authorization[lang],
                    switch_inline_query_current_chat=''
                )]
            ]
        )
