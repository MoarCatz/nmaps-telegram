from functools import wraps

from pony.orm import db_session
from telegram.ext import Filters

from db import User


def private(f):
    @wraps(f)
    def wrapped_private(bot, update, *args, **kwargs):
        if Filters.private.filter(update.message):
            return f(bot, update, *args, **kwargs)
    return wrapped_private


def admins_only(f):
    @wraps(f)
    def wrapped_admins(bot, update, *args, **kwargs):
        with db_session:
            if User.get(user_id=update.effective_user.id).is_admin():
                return f(bot, update, *args, **kwargs)
    return wrapped_admins
