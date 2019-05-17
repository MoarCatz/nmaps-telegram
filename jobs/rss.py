import logging
from calendar import timegm
from itertools import chain
from typing import NoReturn

import feedparser
from pony.orm import db_session
from telegram import Bot, ParseMode
from telegram.error import TelegramError

from bot.config import instantview_url
from bot.models import Rss, Chat, User
from bot.phrases import BOT_NEW_RSS

log_level = logging.INFO

log = logging.Logger("RSS")
log.setLevel(log_level)

log_handler = logging.StreamHandler()
log_handler.setLevel(log_level)

log_fmt = logging.Formatter(
    "[{asctime}] [{levelname}] [RSS]\n{message}\n", datefmt="%d-%m %H:%M:%S", style="{"
)
log_handler.setFormatter(log_fmt)

log.addHandler(log_handler)


def rss(bot: Bot, _job) -> NoReturn:
    log.info("Starting RSS poster")
    new_entries, new_latest_date = get_new_entries()

    with db_session:
        Rss.select().delete()
        Rss(last_published=new_latest_date)

    log.info(f"Wrote latest timestamp to database: {new_latest_date}")

    if new_entries:
        recipients = tuple(chain(Chat.get_subscribers(), User.get_subscribers()))
        log.info("Fetched subscribers")
        log.info("Sending new posts")
        for entry in list(reversed(new_entries)):
            send_post(bot, entry, recipients)
        log.info("Done sending posts!")
    else:
        log.info("No new posts")


def get_new_entries() -> tuple:
    feed = feedparser.parse("https://yandex.ru/blog/narod-karta/rss")
    entries = feed.entries

    with db_session:
        last_published = int(Rss.get().last_published)

    log.info(f"Last published post timestamp is {last_published}")
    new_latest_date = last_published

    new_entries = []
    i = 0
    while timegm(entries[i].published_parsed) > last_published and i < len(entries) - 1:
        if timegm(entries[i].published_parsed) > new_latest_date:
            new_latest_date = timegm(entries[i].published_parsed)
        log.info(f"New entry: {entries[i].link}")
        new_entries.append(entries[i].link)
        i += 1

    return new_entries, new_latest_date


def send_post(bot: Bot, url: str, recipients: tuple) -> NoReturn:
    log.info(f"Sending post: {url}")
    message_text = BOT_NEW_RSS.format(instantview_url.format(url), url)
    for recipient in recipients:
        try:
            bot.send_message(recipient, message_text, parse_mode=ParseMode.MARKDOWN)
        except TelegramError:
            pass
