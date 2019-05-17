import logging
from typing import NoReturn

from telegram import Bot, Update
from telegram.error import TimedOut

# Set logs formatting
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [bot]\n%(message)s",
    datefmt="%d-%m %H:%M:%S",
    level=logging.INFO,
)


def error(_bot: Bot, _update: Update, exc: Exception) -> NoReturn:
    if exc == TimedOut or exc == "Invalid server response":
        return
    logging.error(exc)
