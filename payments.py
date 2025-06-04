from random import randint

import postgres
from misc import bot
from pay_systems.lolzteam import check_lolzteam
from pay_systems.rukassa import check_rukassa


async def generate_payment_comment() -> int:
    while True:
        comment = randint(10 ** 9, 10 ** 10)
        if await postgres.сheck_pay_id(comment):
            break
    return comment


async def check_payments():
    rows = await postgres.check_pay(True)
    for row in rows:
        await check_system(row, True)
    rows = await postgres.check_pay(False)
    for row in rows:
        await check_system(row, False)


async def check_system(row, time):
    if row['system'].lower() == "rukassa":
        if await check_rukassa(row, time):
            await good_pay(row)
        else:
            await bad_pay(row)
    if row['system'].lower() == "lolzteam":
        if await check_lolzteam(row, time):
            await good_pay(row)
        else:
            await bad_pay(row)


async def good_pay(row):
    await postgres.update_pay(row['comment'], row['id_user'], row['amount'])
    await bot.send_message(row['id_user'],
                           f"Платёж номер {row['comment']} пришёл. Баланс пополнен на {row['amount']}")


async def bad_pay(row):
    await postgres.update_pay(row['comment'], ok=False)
    await bot.send_message(row['id_user'], f"Платёж номер {row['comment']} не пришёл. Он больше недоступен!")
