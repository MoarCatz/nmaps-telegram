from pony.orm import db_session
from telegram import ReplyKeyboardMarkup, Update

from config import main_menu
from db import User
from phrases import MENU_SUBSCRIBE, MENU_UNSUBSCRIBE, MENU_ADMIN


@db_session
def get_keyboard(update: Update) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(main_menu.copy(),
                                   one_time_keyboard=True,
                                   resize_keyboard=True)
    user = User.get(user_id=update.effective_user.id)
    if user is None or not user.is_subscribed():
        keyboard.keyboard.append([MENU_SUBSCRIBE])
    else:
        keyboard.keyboard.append([MENU_UNSUBSCRIBE])

    if User.get(user_id=update.effective_user.id).is_admin():
        keyboard.keyboard.append([MENU_ADMIN])

    return keyboard
