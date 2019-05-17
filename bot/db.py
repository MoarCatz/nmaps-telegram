from typing import NoReturn

from pony.orm import Database, db_session
from bot.config import db_creds, nmaps_chat, mods_chat, admins


db = Database(provider="postgres", **db_creds)


def init_db() -> NoReturn:
    from bot.models import Chat, User

    db.generate_mapping(create_tables=True)

    for chat in (nmaps_chat, mods_chat):
        with db_session:
            if not Chat.exists(id=chat):
                Chat(id=chat, name=f"Chat {chat}", subscribed=True)

    for admin_id in admins:
        with db_session:
            if not User.exists(id=admin_id):
                User(id=admin_id, name=f"Admin {admin_id}", admin=True)
            else:
                User[admin_id].admin = True
