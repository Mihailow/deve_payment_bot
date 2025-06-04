from apscheduler.schedulers.asyncio import AsyncIOScheduler

from misc import dp, executor
from handlers import *
from payments import check_payments

scheduler = AsyncIOScheduler()


if __name__ == "__main__":
    scheduler.start()
    scheduler.add_job(check_payments, "interval", seconds=10)
    executor.start_polling(dp, skip_updates=True)
