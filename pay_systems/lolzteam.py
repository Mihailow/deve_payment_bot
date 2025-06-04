from LolzteamApi import LolzteamApi

lolz_token = 'df8d4b25b37a395aa9fbefe82c0709759be68c78'
lolz_user_id = '7620848'
lolz_username = 'bram_mi'

api = LolzteamApi(lolz_token)


async def generate_link(comment, amount):
    link = api.market.payments.generate_link(amount=amount, username=lolz_username, comment=comment)
    return link


async def check_pay(comment, amount):
    answer = api.market.payments.history(user_id=int(lolz_user_id), operation_type='income', pmin=amount, pmax=amount, comment=comment)
    if "errors" not in answer:
        if not answer["payments"]:
            return False
        else:
            return True
    return False


async def check_lolzteam(row, time=True):
    pay = await check_pay(row['comment'], row['amount'])
    if pay:
        return True
    if not time:
        return False
