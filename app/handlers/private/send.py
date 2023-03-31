from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.config import Config
from app.database.googlesheet.sheets_api import GoogleSheet
from app.database.services.repos import UserRepo
from app.handlers.text import Text
from app.keyboards.inline.authorization import auth_kb
from app.keyboards.reply.menu import main_menu_kb, menu_kb
from app.keyboards.reply.send import *
from app.states.states import SendSG


def is_number(msg: Message):
    return str(msg.text).isnumeric()


async def send_points(msg: Message, state: FSMContext, user_db: UserRepo):
    user = await user_db.get_user(msg.from_user.id)
    if user.gift_points == 0:
        await msg.answer(Text.send.limit_over[user.lang], reply_markup=main_menu_kb(user.lang))
        return
    await msg.answer(Text.send.list_of_people[user.lang], reply_markup=send_kb(user.lang))
    await state.update_data(gefter_id=msg.from_user.id)


async def select_user(msg: Message, user_db: UserRepo, google_sheet: GoogleSheet, config: Config):
    me = await user_db.get_user(msg.from_user.id)
    # commands = google_sheet.get_commands(config.misc.user_spreadsheet_id)
    # await msg.answer(Text.send.select_command[me.lang], reply_markup=select_user_commands(commands, me.lang))
    exist_users = []
    for user in await user_db.get_authorized_user():
        # if google_sheet.get_user(config.misc.user_spreadsheet_id, user.auth_data):
        exist_users.append(user)
    # await msg.answer(Text.send.select_user[me.lang],
    #                  reply_markup=select_user_commands(commands, me.lang))
    await msg.answer(Text.send.select_user[me.lang],
                     reply_markup=await select_user_kb(exist_users, me.full_name, lang=me.lang))
    await msg.answer(Text.send.search_people[me.lang], reply_markup=auth_kb('Email', me.lang))
    await SendSG.User.set()


# async def select_user(msg: Message, user_db: UserRepo, google_sheet: GoogleSheet, config: Config):
#     lang = await user_db.get_user(msg.from_user.id)
#     users = await user_db.get_authorized_user()
#     users.remove(await user_db.get_user(msg.from_user.id))
#     exist_users = []
#     for user in users:
#         google_sheet_user = google_sheet.get_user(config.misc.user_spreadsheet_id, user.auth_data)
#         if google_sheet_user and google_sheet_user[-1] in msg.text:
#             exist_users.append(user)
#     await msg.answer(Text.send.select_user[lang],
#                      reply_markup=await select_user_kb(exist_users, lang=lang))
#     await SendSG.User.set()


async def save_user(msg: Message, state: FSMContext, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    user = await user_db.get_user_by_name(msg.text)
    if user is None:
        await msg.answer(Text.send.not_found_user[lang], reply_markup=auth_kb('Email', lang))
        return
    if user.user_id == msg.from_user.id:
        await msg.answer(Text.send.send_to_self[lang])
        return
    await state.update_data(name=msg.text)
    await msg.answer(Text.send.word_of_thanks[lang], reply_markup=main_menu_kb(lang))
    await SendSG.Message.set()


async def save_message(msg: Message, state: FSMContext, user_db: UserRepo):
    await state.update_data(message=msg.text)
    user = await user_db.get_user(msg.from_user.id)
    await msg.answer(Text.send.how_much_coins[user.lang].format(user.gift_points))
    await SendSG.Points.set()


async def save_points(msg: Message, user_db: UserRepo, state: FSMContext):
    user = await user_db.get_user(msg.from_user.id)
    if not is_number(msg):
        return await msg.answer(Text.send.not_a_number[user.lang])
    elif int(msg.text) > user.gift_points:
        return await msg.answer(Text.send.you_only_have[user.lang].format(user.gift_points))
    elif int(msg.text) <= 0:
        return await msg.answer(Text.send.too_small[user.lang])
    await state.update_data(points=int(msg.text))
    await msg.answer(text=Text.send.reg_coins[user.lang].format(msg.text), reply_markup=values_kb(user.lang))
    await state.update_data(value='')
    await SendSG.Value.set()


async def input_values(msg: Message, state: FSMContext, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    data = await state.get_data()
    value = data['value']
    if value == '':
        values = [msg.text]
    else:
        value.append(msg.text)
        values = value
    values_str = ', '.join(values)
    await state.update_data(value=values)
    await msg.answer(Text.send.select_values[lang].format(values_str),
                     reply_markup=values_kb(next_button=True, added_values=values, lang=lang))


async def input_custom_value(msg: Message, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    await msg.answer(Text.send.what_a_value[lang])
    await SendSG.CustomValue.set()


async def confirm(msg: Message, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    await msg.answer(Text.send.all_is_good[lang], reply_markup=confirm_send_kb(lang))
    await SendSG.Confirm.set()


async def send(msg: Message, user_db: UserRepo, point_db: PointRepo,
               state: FSMContext, config: Config, google_sheet: GoogleSheet):
    lang = await user_db.get_language(msg.from_user.id)
    state_data = await state.get_data()
    name = state_data['name']
    points = int(state_data['points'])
    message = state_data['message']
    value = ', '.join(state_data['value'])
    gifter = await user_db.get_user(msg.from_user.id)
    user = await user_db.get_user_by_name(name)
    await point_db.add(
        user_id=user.user_id, gifter_id=gifter.user_id,
        scale=points, value=value, comment=message
    )
    remain_points = gifter.gift_points - points
    await user_db.update_user(gifter.user_id, gift_points=remain_points)
    answer_text = Text.send.thank_for[lang]
    if remain_points == 0:
        answer_text += Text.send.use_all_coins[lang]
        await msg.answer(answer_text, reply_markup=main_menu_kb(lang))
    else:
        answer_text += Text.send.coins_remain[lang].format(remain_points)
        await msg.answer(answer_text, reply_markup=menu_kb(lang))
    await msg.bot.send_message(user.user_id, text=Text.send.message_thank[user.lang].format(points, gifter.full_name, value, message))
    await state.finish()
    # await send_points(msg, state, user_db)
    await state.update_data(gefter_id=msg.from_user.id)
    google_sheet.write_event(
        spreadsheet_id=config.misc.user_spreadsheet_id,
        action='Переказ балів',
        sender_name=gifter.full_name,
        getter_name=user.full_name,
        points=points,
        val=value, message=message, sheet_name='Send'
    )


def setup(dp: Dispatcher):
    dp.register_message_handler(send_points, text=[Buttons.menu.send_points['ua'], Buttons.menu.send_points['ru']],
                                state='*')
    # dp.register_message_handler(select_command, ],
    #                             state='*')
    dp.register_message_handler(select_user, text=[Buttons.send.select_user['ua'], [Buttons.send.select_user['ru']]],
                                state='*')
    dp.register_message_handler(save_user, state=SendSG.User)
    dp.register_message_handler(save_message, state=SendSG.Message)
    dp.register_message_handler(save_points, state=SendSG.Points)
    dp.register_message_handler(input_custom_value, state=[SendSG.Value, SendSG.CustomValue],
                                text=[Buttons.send.custom_value['ua'], Buttons.send.custom_value['ru']])
    dp.register_message_handler(confirm, state=[SendSG.Value, SendSG.CustomValue],
                                text=[Buttons.send.next_button['ua'], Buttons.send.next_button['ru']])
    dp.register_message_handler(input_values, state=[SendSG.Value, SendSG.CustomValue])
    dp.register_message_handler(send, state=SendSG.Confirm)

