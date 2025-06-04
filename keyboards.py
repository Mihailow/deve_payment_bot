from postgres import get_payment_systems_names

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


async def main_keyboard():
    keyboard = [
        [KeyboardButton(text="Мой профиль")],
        [KeyboardButton(text="Пополнить баланс")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard)


async def pay_systems_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    table = await get_payment_systems_names()
    for line in table:
        keyboard.add(InlineKeyboardButton(text=line['name'], callback_data="sys_"+line['name']))
    return keyboard


async def url_keyboard(url):
    keyboard = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='ссылка на оплату', url=url))
    return keyboard


async def back_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Назад', callback_data='pay_back'))
    return keyboard
