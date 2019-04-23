from pony.orm import PrimaryKey, Required, Optional

from bot.db import db


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


class Chat(db.Entity):
    id = PrimaryKey(int, auto=True)
    chat_id = Required(int, size=64)
    name = Required(str)
    subscribed = Required(bool, sql_default='FALSE')
