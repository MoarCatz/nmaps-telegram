from typing import NoReturn

from pony.orm import db_session
from telegram.bot import Bot, Update
from telegram.ext import MessageHandler, Filters

from bot.models import Chat, User, Subscriber
from typing import Type


def checkin(_bot: Bot, update: Update) -> NoReturn:
    is_chat = False if update.effective_chat.type == "private" else True
    track_sub_name(User, update.effective_user.id, update.effective_user.name)
    if is_chat:
        track_sub_name(Chat, update.effective_chat.id, update.effective_chat.title)


@db_session
def track_sub_name(cls: Type[Subscriber], sub_id: int, sub_name: str):
    if not cls.exists(id=sub_id):
        cls.add(sub_id, sub_name)
    sub: Subscriber = cls.get(id=sub_id)
    if sub_name != sub.name:
        sub.previous_names.append(sub.name)
        sub.name = sub_name


checkin_handler = MessageHandler(Filters.all, checkin)
