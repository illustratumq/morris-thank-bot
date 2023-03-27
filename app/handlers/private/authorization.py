from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineQuery

from app.config import Config
from app.database.googlesheet.sheets_api import GoogleSheet
from app.database.services.enums import UserStatusEnum
from app.database.services.repos import UserRepo
from app.filters.auth import IsEmailMethod
from app.handlers.text import Text
from app.keyboards import Buttons
from app.keyboards.inline.authorization import auth_kb, lang_kb
from app.keyboards.reply.menu import to_menu_kb
from app.states.states import AuthSG, SendSG, DeleteSG


async def repeat_authorization_cmd(msg: Message, config: Config, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    await msg.answer(Text.auth.auth, reply_markup=auth_kb(config.misc.auth_method, lang))
    await AuthSG.AuthData.set()


async def authorization_cmd(msg: Message, user_db: UserRepo):
    await user_db.add(
        user_id=msg.from_user.id,
        full_name=msg.from_user.full_name,
        mention=msg.from_user.mention, status=UserStatusEnum.UNAUTHORIZED
    )
    text = (
        'Оберіть, будь ласка, мову'
    )
    await msg.answer(text, reply_markup=lang_kb)
    await AuthSG.Lang.set()


async def language_cmd(msg: Message, config: Config, user_db: UserRepo):
    if msg.text == 'Російська':
        lang = 'ru'
    else:
        lang = 'ua'
    await user_db.update_user(msg.from_user.id, lang=lang)
    await msg.answer(Text.auth.greeting[lang], reply_markup=auth_kb(config.misc.auth_method, lang))
    await AuthSG.AuthData.set()


async def save_user_email(msg: Message, user_db: UserRepo, state: FSMContext,
                          config: Config, google_sheet: GoogleSheet):
    lang = await user_db.get_language(msg.from_user.id)
    email = msg.text.strip()
    google_sheet_user = google_sheet.get_user(config.misc.user_spreadsheet_id, auth_data=email)
    if google_sheet_user:

        user_same_email = await user_db.get_user_by_auth_data(email)
        if user_same_email:
            await msg.answer(Text.auth.email_is_busy[lang].format(user_same_email.full_name))
            return
        await user_db.update_user(
            user_id=msg.from_user.id,
            full_name=google_sheet_user[0],
            auth_data=email,
            mention=create_custom_mention(google_sheet_user[0], msg.from_user.id),
            status=UserStatusEnum.AUTHORIZED
        )
        await msg.answer(Text.auth.your_name_is[lang].format(google_sheet_user[0]), reply_markup=to_menu_kb(lang))
        # google_sheet.write_event(
        #     spreadsheet_id=config.misc.user_spreadsheet_id,
        #     action='Авторизація в боті',
        #     sender_name='Від бота',
        #     getter_name=google_sheet_user[0],
        #     points=100,
        #     val='Користувач', message='Початкове нарахування', sheet_name='Registration'
        # )
        await state.finish()
    else:
        await msg.answer(Text.auth.email_not_found[lang], reply_markup=auth_kb(config.misc.auth_method, lang))


async def query_user_list(query: InlineQuery, google_sheet: GoogleSheet, config: Config, state: FSMContext):
    query_text = str(query.query).lower()
    sheet_users = google_sheet.get_auth_data(config.misc.user_spreadsheet_id)
    await state.update_data(sheet_users=sheet_users)
    results = []
    if query_text != '':
        for user in sheet_users:
            full_name, auth_data = user
            if auth_data.isnumeric():
                if query_text in auth_data:
                    results.append(create_article(*user))
            elif auth_data.lower().startswith(query_text):
                results.append(create_article(*user))
    if results:
        await query.answer(results=results[:5], is_personal=True)


async def query_username_list(query: InlineQuery, google_sheet: GoogleSheet, config: Config):
    query_text = str(query.query)
    sheet_users = google_sheet.get_auth_data(config.misc.user_spreadsheet_id)
    results = []
    if query_text != '':
        for user in sheet_users:
            first_name, second_name = user[0].split(' ')
            if query_text.lower() in first_name.lower() or query_text.lower() in second_name.lower():
                results.append(create_article(*user, username=True))
    if results:
        await query.answer(results=results[:5], is_personal=True)


def setup(dp: Dispatcher):
    dp.register_message_handler(language_cmd, text=['Російська', 'Українська'], state=AuthSG.Lang)
    dp.register_message_handler(repeat_authorization_cmd, text=[Buttons.menu.auth_bt['ua'], Buttons.menu.auth_bt['ru']],
                                state='*')
    dp.register_message_handler(save_user_email,  IsEmailMethod(), state=AuthSG.AuthData)
    dp.register_inline_handler(query_user_list, state=AuthSG.all_states)
    dp.register_inline_handler(query_username_list, state=[SendSG.User, DeleteSG.User])


def create_article(full_name, auth_data, username: bool = False):
    return types.InlineQueryResultArticle(
        id=auth_data,
        title=full_name,
        description=auth_data,
        input_message_content=types.InputTextMessageContent(
            message_text=full_name if username else auth_data
        )
    )


def create_custom_mention(name: str, user_id: int) -> str:
    return f'<a href="tg://user?id={str(user_id)}">{name}</a>'


