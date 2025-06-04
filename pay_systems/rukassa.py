import aiohttp
import json

rukassa_token = "a709237437d7cb23c7ed49d688896620"
rukassa_shop_id = "1338"


async def generate_link(id_pay, amount):
    url = 'https://lk.rukassa.pro/api/v1/create'
    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                params={'shop_id': rukassa_shop_id, 'order_id': id_pay, 'amount': amount, 'token': rukassa_token}) as resp:
            response = await resp.read()
            json_str = json.loads(response)
            return json_str


async def check_pay(id_pay):
    url = 'https://lk.rukassa.pro/api/v1/getPayInfo'
    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                params={'id': id_pay, 'shop_id': rukassa_shop_id, 'token': rukassa_token}) as resp:
            response = await resp.read()
            json_str = json.loads(response)
            return json_str['status']


async def check_rukassa(row, time=True):
    pay = await check_pay(row['additionally'])
    if pay == 'PAID':
        return True
    if not time:
        return False
