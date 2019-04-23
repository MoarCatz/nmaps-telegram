from pony.orm import db_session
from telegram.bot import Bot, Update, User

from bot.models import Chat, User as U


@db_session
def add_user(_bot: Bot, update: Update) -> None:
    user: User = update.effective_user
    if not U.exists(user_id=user.id):
        U(user_id=user.id, name=user.name)
    U.get(user_id=user.id).name = user.name


@db_session
def add_chat(_bot: Bot, update: Update) -> None:
    chat_id = update.effective_chat.id
    if not Chat.exists(chat_id=chat_id):
        Chat(chat_id=chat_id, name=update.effective_chat.title)
    Chat.get(chat_id=chat_id).name = update.effective_chat.title
