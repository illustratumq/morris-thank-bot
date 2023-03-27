from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.database.services.enums import UserStatusEnum
from app.database.services.repos import UserRepo, PointRepo
from app.handlers.private.authorization import authorization_cmd
from app.handlers.text import Text
from app.keyboards.reply.menu import menu_kb, Buttons, to_auth


async def start_cmd(msg: Message, user_db: UserRepo, state: FSMContext):
    user = await user_db.get_user(msg.from_user.id)
    if not user:
        await authorization_cmd(msg, user_db)
    elif user.status == UserStatusEnum.UNAUTHORIZED:
        await msg.answer(Text.start.not_complete_auth[user.lang], reply_markup=to_auth(user.lang))
    else:
        await state.finish()
        await msg.answer(Text.start.complete_auth[user.lang], reply_markup=menu_kb(user.lang))


async def after_registration_greeting(msg: Message, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    await msg.answer(Text.start.after_auth_text[lang], reply_markup=menu_kb(lang))


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
    dp.register_message_handler(after_registration_greeting, text=Buttons.menu.go_next['ua'] + Buttons.menu.go_next['ru'],
                                state='*')
    dp.register_message_handler(start_cmd, text=[Buttons.menu.main_menu['ua'], Buttons.menu.main_menu['ru']],
                                state='*')


async def users_rating(user_db: UserRepo, point_db: PointRepo) -> list:
    users = await user_db.get_all()
    rating = []
    for user in users:
        rating.append(dict(user_id=user.user_id, point=await point_db.get_user_points(user.user_id, count=True)))
    rating.sort(key=lambda usr: usr['point'], reverse=True)
    return [int(usr['user_id']) for usr in rating]
