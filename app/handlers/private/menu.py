from aiogram import Dispatcher
from aiogram.types import Message

from app.database.services.repos import UserRepo, PointRepo
from app.keyboards.reply.menu import main_menu_kb, Buttons, my_profile_kb


rules_str_ua = '''Вдячність має велику силу! За допомогою цього простору ми прагнемо зробити Практику Вдячності простою, фановою та приємною! 
🧡 На початку кожного місяця ти будеш отримувати 100 wellcoin-ів. Кількість wellcoin-ів до своїх подяк ти можеш розподіляти на власний розсуд.

🔹 Як передати wellcoin-ни?
1 - вибери колегу, кому ти хочеш подякувати
2 - напиши теплі слова вдячності
3 - вкажи, за яку саме цінність ти вдячна/-ний?
4 - вкажи кількість wellcoin-ів, які хочеш додати.

В кінці місяця ми визначимо переможця, який зібрав найбільшу кількість wellcoin-ів за свої добрі вчинки❤'''


rules_str_ru = '''Благодарность имеет большую силу! С помощью этого пространства мы стремимся сделать Практику признательности простой, фановой и приятной!
🧡 В начале каждого месяца ты будешь получать 100 wellcoin-ов. Количество wellcoin-ов к своим благодарностям ты можешь распределять по собственному усмотрению.

🔹 Как передать wellcoin-ны?
1 - выбери коллегу, кого ты хочешь поблагодарить
2 – напиши теплые слова благодарности
3 - укажи, за какую именно ценность ты благодарен/а?
4 – укажи количество wellcoin-ов, которые хочешь добавить.

В конце месяца мы определим победителя, собравшего наибольшее количество wellcoin-ов за свои добрые поступки❤'''


async def profile(msg: Message, user_db: UserRepo, point_db: PointRepo):
    user = await user_db.get_user(msg.from_user.id)
    points = await point_db.get_user_points(user.user_id, count=True)
    points_this_month = await point_db.get_user_points(user.user_id, count=True, this_month=True)
    text_ua = (
        f'<b>Отримані wellcoin-и 💚</b>\n'
        f'В цьому місяці: {points_this_month}\n'
        f'За весь період: {points}\n\n'
        f'<b>В цьому місяці ти можеш ще віддати: {user.gift_points}💚</b>'
    )
    text_ru = (
        f'<b>Полученые wellcoin-ы 💚</b>\n'
        f'В этом месяце: {points_this_month}\n'
        f'За весь период: {points}\n\n'
        f'<b>В этом месяце ты можешь еще отдать: {user.gift_points}💚</b>'
    )
    await msg.answer(text_ua if user.lang == 'ua' else text_ru, reply_markup=my_profile_kb(user.lang))


async def rules(msg: Message, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    await msg.answer(rules_str_ua if lang == 'ua' else rules_str_ru, reply_markup=main_menu_kb(lang))


async def info(msg: Message, user_db: UserRepo):
    lang = await user_db.get_language(msg.from_user.id)
    text_ua = (
        'Стаття "5 переваг вдячності для здоров\'я"💚\n\n'
        'Реальні дослідження, які показують позитивний вплив '
        'на наше здоров\'я та самопочуття:\n\nhttps://www.wellright.com/blog/5-wellness-benefits-of-gratitude '
    )
    text_ru = (
         'Статья "5 преимуществ благодарности для здоровья"💚\n\n'
         'Реальные исследования, показывающие положительное влияние '
         'на наше здоровье и самочувствие:\n\nhttps://www.wellright.com/blog/5-wellness-benefits-of-gratitude '
     )
    await msg.answer(text_ua if lang == 'ua' else text_ru, reply_markup=main_menu_kb(lang))


def setup(dp: Dispatcher):
    dp.register_message_handler(profile, text=[Buttons.menu.my_profile['ua'], Buttons.menu.my_profile['ru']],
                                state='*')
    dp.register_message_handler(rules, text=[Buttons.menu.rules['ua'], Buttons.menu.rules['ru']],
                                state='*')
    dp.register_message_handler(info, text=[Buttons.menu.info['ua'], Buttons.menu.info['ru']], state='*')
