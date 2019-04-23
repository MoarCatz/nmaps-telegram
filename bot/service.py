from typing import NoReturn

from pony.orm import db_session

from bot.config import nmaps_chat, mods_chat, admins
from bot.db import db
from bot.models import Chat, User


def init_db() -> NoReturn:
    for chat in (nmaps_chat, mods_chat):
        with db_session:
            if not Chat.exists(chat_id=chat):
                Chat(chat_id=chat,
                     name=f"Chat {chat}",
                     subscribed=True)

    for admin_id in admins:
        with db_session:
            if not User.exists(user_id=admin_id):
                User(user_id=admin_id,
                     name=f"Admin {admin_id}",
                     admin=True)
            else:
                User[admin_id].admin = True

    db.generate_mapping(create_tables=True)
