from config import DB_HOST, DB_NAME, DB_USER, DB_PASS, telegram_token

import psycopg2
import psycopg2.extras


async def postgres_init_connection(HOST, DATABASE, USER, PASSWORD):
    global DB_HOST, DB_NAME, DB_USER, DB_PASS
    DB_HOST = HOST
    DB_NAME = DATABASE
    DB_USER = USER
    DB_PASS = PASSWORD


async def postgres_do_query(query, params):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()
    return None


async def postgres_select_one(query, params):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, params)
    result = cursor.fetchone()
    if result:
        result = dict(result)
    conn.commit()
    cursor.close()
    conn.close()

    return result


async def postgres_select_all(query, params):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, params)
    results = cursor.fetchall()
    if results:
        res = []
        for r in results:
            res.append(dict(r))
        results = res
    conn.commit()
    cursor.close()
    conn.close()
    return results


async def get_payment_systems(system):
    return await postgres_select_all("SELECT * FROM connected_payment_systems WHERE bot_token = %s AND system = %s", (telegram_token, system,))


async def get_payment_systems_names():
    return await postgres_select_all("SELECT name FROM connected_payment_systems WHERE bot_token = %s", (telegram_token,))


async def insert_user(user_id):
    if await postgres_select_one("SELECT user_id FROM users WHERE user_id = %s AND token = %s", (user_id, telegram_token)) is None:
        await postgres_do_query("INSERT INTO users (token, user_id, balance) "
                                "VALUES (%s, %s, %s)",
                                (telegram_token, user_id, 0,))


async def show_profile(user_id):
    records = await postgres_select_one("SELECT user_id, balance FROM users WHERE user_id = %s AND token = %s", (user_id, telegram_token))
    ret = "id: " + str(records['user_id']) + "\nБаланс: " + str(records['balance'])
    return ret


async def сheck_pay_id(comment):
    if await postgres_select_one("SELECT comment FROM payments WHERE comment = %s AND token = %s", (str(comment), telegram_token)) is None:
        return True
    return False


async def insert_pay(id_user, amount, comment, system, additionally=None):
    await postgres_do_query(
        "INSERT INTO payments (token, id_user, amount, status, comment, date, system, additionally) "
        "VALUES (%s, %s, %s, 'formed', %s, NOW(), %s, %s)",
        (telegram_token, id_user, amount, comment, system, additionally,))


async def check_pay(ok):
    if ok:
        return await postgres_select_all(
            "SELECT * FROM payments WHERE NOW()-date < interval '1 hour' AND status = 'formed' AND token = %s", (telegram_token, ))
    return await postgres_select_all(
        "SELECT * FROM payments WHERE NOW()-date > interval '1 hour' AND status = 'formed' AND token = %s", (telegram_token, ))


async def update_pay(comment, user_id=None, amount=None, ok=True):
    if ok:
        await postgres_do_query("UPDATE payments SET status = 'completed' WHERE comment = %s AND token = %s", (comment, telegram_token,))
        await postgres_do_query("UPDATE users SET balance = balance+%s WHERE user_id = %s AND token = %s", (amount, user_id, telegram_token,))
    else:
        await postgres_do_query("UPDATE payments SET status = 'canceled' WHERE comment = %s AND token = %s", (comment, telegram_token,))
