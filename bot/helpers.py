from functools import wraps

from pony.orm import db_session
from telegram import ReplyKeyboardMarkup, Update, Bot
from telegram.ext import Filters, ConversationHandler

from bot.config import main_menu
from bot.models import User
from bot.phrases import MENU_SUBSCRIBE, MENU_UNSUBSCRIBE, MENU_ADMIN, BOT_CANCELLED


@db_session
def get_keyboard(update: Update) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(main_menu.copy(),
                                   one_time_keyboard=True,
                                   resize_keyboard=True)
    user = User[update.effective_user.id]
    if user is None or not user.subscribed:
        keyboard.keyboard.append([MENU_SUBSCRIBE])
    else:
        keyboard.keyboard.append([MENU_UNSUBSCRIBE])

    if User[update.effective_user.id].admin:
        keyboard.keyboard.append([MENU_ADMIN])

    return keyboard


def admins_only(f):
    @wraps(f)
    def wrapped_admins(bot, update, *args, **kwargs):
        with db_session:
            if User[update.effective_user.id].admin:
                return f(bot, update, *args, **kwargs)
    return wrapped_admins


def private(f):
    @wraps(f)
    def wrapped_private(bot, update, *args, **kwargs):
        if update.callback_query or Filters.private.filter(update.message):
            return f(bot, update, *args, **kwargs)
    return wrapped_private


@private
def cancel(_bot: Bot, update: Update, user_data: dict) -> int:
    update.message.reply_text(
        BOT_CANCELLED,
        reply_markup=get_keyboard(update))
    user_data.clear()
    return ConversationHandler.END
