from telegram.ext import Updater

from bot.config import *
from bot.db import init_db
from bot.devmode import enable_dev, get_headers
from bot.logger import error
from handlers import handlers, checkin_handler
from jobs.rss import rss

# Setup
updater = Updater(telegram_key, request_kwargs=get_headers())
dp = updater.dispatcher
jobs = updater.job_queue

# Register handlers
dp.add_handler(checkin_handler, group=0)
for handler in handlers:
    dp.add_handler(handler, group=1)

# Register loggers
dp.add_error_handler(error)

# Register jobs
if not enable_dev():
    jobs.run_repeating(rss, 300)


if __name__ == "__main__":
    init_db()

    # Actually start the bot
    updater.start_polling()
    updater.idle()
