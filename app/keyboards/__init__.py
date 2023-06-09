from dataclasses import dataclass


@dataclass()
class Admin:
    statistic: str = 'Статистика 📊'
    rating: str = 'Рейтинг 🏆'
    delete: str = 'Видалити користувача 🚫'
    update: str = 'Оновити користувачів 🔄'
    phones: str = 'Номера телефону'
    names: str = 'Ім\'я користувачів'
    back: str = 'Повернутись ↩'


@dataclass()
class Auth:
    authorization = {'ua': 'Шукати 🔍', 'ru': 'Искать 🔍'}


class Menu:
    send_points = {'ua': 'Віддати подяку 📬', 'ru': 'Отдать благодарность 📬'}
    my_profile = {'ua': 'Мій профіль 💚', 'ru': 'Мой профиль 💚'}
    rules = {'ua': 'Правила 📃', 'ru': 'Правила 📃'}
    info = {'ua': 'Цікаві матеріали про вдячність', 'ru': 'Материалы о благодарности'}
    user_rating = {'ua': 'Рейтинг 🏆', 'ru': 'Рейтинг 🏆'}
    go_next = {
        'ua': ['Так 🥰'],
        'ru': ['Да 🥰'],
    }
    history = {'ua': 'Моя історія 📚', 'ru': 'Моя история 📚'}
    main_menu = {'ua': 'В головне меню ↩', 'ru': 'В главное меню ↩'}
    my_send = {'ua': 'Мої перекази ✉', 'ru': 'Мои переводы ✉'}
    to_me_send = {'ua': 'Перекази для мене 📩', 'ru': 'Переводы для меня 📩'}
    back_to_history = {'ua': '⬅ Назад', 'ru': '⬅ Назад'}
    auth_bt = {'ua': 'Авторизуватись ✔', 'ru': 'Авторизоваться ✔'}
    share_phone = {'ua': 'Поділитися телефоном 📲', 'ru': 'Подлиться телефоном 📲'}

    auth: Auth = Auth()


class Send:
    select_user = {'ua': 'Список колег', 'ru': 'Список колег'}
    confirm = {'ua': 'Так, відправити ✅', 'ru': 'Да, отправить ✅'}
    custom_value = {'ua': 'Свій варіант', 'ru': 'Свой вариант'}
    next_button = {'ua': '✅ Відправити wellcoin-и', 'ru': '✅ Отправить wellcoin-ы'}

    @staticmethod
    def values(lang: str):
        if lang == 'ua':
            return ['Added value', 'Розвиток', 'Забота та повага', 'Ефективність']
        else:
            return ['Added value', 'Развитие', 'Забота и уважение', 'Эффективность']


@dataclass
class Buttons:
    menu = Menu()
    send = Send()
    admin = Admin()
