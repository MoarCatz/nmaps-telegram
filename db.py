import os
from pony.orm import Database, PrimaryKey, Required, Optional, db_session

from config import nmaps_chat, mods_chat, roads_chat, admins


db_creds = {'host': os.getenv('DBHOST', 'localhost'),
            'database': os.getenv('DBNAME', 'bot'),
            'user': os.getenv('DBUSER', 'bot'),
            'password': os.getenv('DBPASS', 'bot')}

db = Database(provider='postgres', **db_creds)


class Roadblock(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(int, size=64)
    chat_id = Required(int, size=64)
    chat_message_id = Required(int, size=64)
    mods_message_id = Optional(int, size=64)
    roads_message_id = Optional(int, size=64)


class Rss(db.Entity):
    id = PrimaryKey(int, auto=True)
    last_published = Required(int, size=64)


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_id = Required(int, size=64, unique=True)
    name = Required(str)
    roadblocks_count = Required(int, sql_default='0')
    admin = Required(bool, sql_default='FALSE')
    banned = Required(bool, sql_default='FALSE')
    subscribed = Required(bool, sql_default='FALSE')

    def is_subscribed(self) -> bool:
        return self.subscribed

    def is_admin(self) -> bool:
        return self.admin

    def is_banned(self) -> bool:
        return self.banned


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    chat_id = Required(int, size=64)
    name = Required(str)
    subscribed = Required(bool, sql_default='FALSE')

    def is_subscribed(self) -> bool:
        return self.subscribed


db.generate_mapping(create_tables=True)

for chat in (nmaps_chat, mods_chat):
    with db_session:
        if not Chat.exists(chat_id=chat):
            Chat(chat_id=chat, name="Chat {}".format(chat), subscribed=True)

for admin in admins:
    with db_session:
        if not User.exists(user_id=admin):
            User(user_id=admin, name="Admin {}".format(admin), admin=True)
        else:
            User.get(user_id=admin).admin = True
