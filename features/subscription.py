from phrases import BOT_SUBSCRIBED_USR, BOT_UNSUBSCRIBED_USR
from helpers import get_keyboard
from telegram import Bot, Update

from pony.orm import db_session
from db import Chat, User


@db_session
def update_subscription(_bot: Bot, update: Update) -> None:
    user_id = update.effective_user.id

    if not User.get(user_id=user_id).is_subscribed():
        subscribe_user(user_id)
        update.message.reply_text(BOT_SUBSCRIBED_USR,
                                  reply_markup=get_keyboard(update))
    else:
        unsubscribe_user(user_id)
        update.message.reply_text(BOT_UNSUBSCRIBED_USR,
                                  reply_markup=get_keyboard(update))


@db_session
def subscribe_user(user_id: int) -> None:
    User.get(user_id=user_id).subscribed = True


@db_session
def unsubscribe_user(user_id: int) -> None:
    User.get(user_id=user_id).subscribed = False


@db_session
def subscribe_chat(chat_id: int) -> None:
    Chat.get(chat_id=chat_id).subscribed = True


@db_session
def unsubscribe_chat(chat_id: int) -> None:
    Chat.get(chat_id=chat_id).subscribed = False
