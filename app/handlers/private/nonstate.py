from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.database.services.repos import UserRepo
from app.keyboards.reply.menu import main_menu_kb


async def non_state_message(msg: Message, state: FSMContext, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    text_ru = (
        'Чат-бот запрограммирован на общение кнопками 😉\n'
        'Написанный вручную текст не обрабатывается. '
        'Чтобы продолжить диалог, нажмите кнопку "Главное меню"\n\n'
        'В случае возникновения проблем нажмите /start'
    )
    text_ua = (
        'Чат-бот запрограмований на спілкування кнопками 😉\n'
        'Написаний вручну текст не обробляється. '
        'Щоб продовжити діалог, натисніть на кнопку "Головне меню"\n\n'
        'У разі виникнення проблем, натисніть команду /start'
    )
    await msg.answer(
        text_ua if lang == 'ua' else text_ru,
        reply_markup=main_menu_kb(lang)
    )
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_message_handler(non_state_message, state='*')
