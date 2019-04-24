from pony.orm import PrimaryKey, Required, Optional, Set, StrArray

from bot.db import db
from typing import NoReturn, List


class Rss(db.Entity):
    id = PrimaryKey(int, auto=True)
    last_published = Required(int, size=64)


class Subscriber(db.Entity):
    id = PrimaryKey(int, size=64)
    name = Required(str)
    previous_names = Optional(StrArray)
    subscribed = Required(bool, sql_default="FALSE")

    def subscribe(self) -> NoReturn:
        self.subscribed = True

    def unsubscribe(self) -> NoReturn:
        self.subscribed = False

    def update_subscription(self) -> NoReturn:
        self.subscribed = True if not self.subscribed else False

    @classmethod
    def add(cls, subscriber_id: int, name: str) -> NoReturn:
        cls(id=subscriber_id, name=name)

    @classmethod
    def get_subscribers(cls) -> List[int]:
        return User.select(lambda s: s.subscribed)


class User(Subscriber):
    admin = Required(bool, sql_default="FALSE")
    banned = Required(bool, sql_default="FALSE")
    roadblocks = Set(lambda: Roadblock)


class Chat(Subscriber):
    pass


class Roadblock(db.Entity):
    id = PrimaryKey(int, auto=True)
    author = Required(User)
    chat_id = Required(int, size=64)
    chat_message_id = Required(int, size=64)
    mods_message_id = Optional(int, size=64)
    roads_message_id = Optional(int, size=64)
