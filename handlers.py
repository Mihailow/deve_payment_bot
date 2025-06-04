from aiogram import types
from aiogram.dispatcher import FSMContext

import postgres
from pay_systems import rukassa, lolzteam
from keyboards import *
from main import dp
from misc import bot, Status
from payments import generate_payment_comment


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await postgres.insert_user(message.from_user.id)
    await message.answer("Добро пожаловать!", reply_markup=await main_keyboard())
    return


@dp.message_handler(text="Мой профиль")
async def my_profile(message: types.Message):
    await message.answer(await postgres.show_profile(message.from_user.id))
    return


@dp.message_handler(text="Пополнить баланс")
async def add_money(message: types.Message):
    await message.answer("Выберите систему оплаты", reply_markup=await pay_systems_keyboard())
    return


@dp.callback_query_handler(text='sys_RuKassa')
async def sys_rukassa(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer("Введите сумму для оплаты\nСумма должна быть больше 100!",
                                        reply_markup=await back_keyboard())
    await Status.rukassa.set()
    return


@dp.callback_query_handler(text='sys_Lolzteam')
async def sys_lolzteam(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer("Введите сумму для оплаты\nСумма должна быть без копеек!",
                                        reply_markup=await back_keyboard())
    await Status.lolzteam.set()
    return


@dp.callback_query_handler(state='*', text='pay_back')
async def pay_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer("Выберите систему оплаты", reply_markup=await pay_systems_keyboard())
    await state.finish()
    return


@dp.message_handler(state=Status.rukassa)
async def status_rukassa(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount < 100:
            await message.answer("Сумма должна быть больше 100!", reply_markup=await back_keyboard())
            return
    except:
        await message.answer("Сумма введена неправильно!", reply_markup=await back_keyboard())
        return
    comment = await generate_payment_comment()
    url = await rukassa.generate_link(comment, amount)
    await message.answer(
        "!ВАЖНО!\n\nВаша ссылка будет действительна в течении часа!",
        reply_markup=await url_keyboard(url['url']))
    await postgres.insert_pay(message.from_user.id, amount, comment, 'RuKassa', url['id'])
    await state.finish()


@dp.message_handler(state=Status.lolzteam)
async def status_lolzteam(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
    except:
        await message.answer("Сумма введена неправильно!", reply_markup=await back_keyboard())
        return
    comment = await generate_payment_comment()
    url = await lolzteam.generate_link(comment, amount)
    await message.answer(
        "!ВАЖНО!\n\nНе меняйте сумму оплаты и комментарий, иначе зачисление не будет произведено!\n\n"
        "Ваша ссылка будет действительна в течении часа!",
        reply_markup=await url_keyboard(url))
    await postgres.insert_pay(message.from_user.id, amount, comment, 'Lolzteam')
    await state.finish()
