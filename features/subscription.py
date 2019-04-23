from pony.orm import db_session
from telegram import Bot, Update

from bot.helpers import get_keyboard, private
from bot.models import User
from bot.phrases import BOT_SUBSCRIBED_USR, BOT_UNSUBSCRIBED_USR


@private
@db_session
def update_subscription(_bot: Bot, update: Update) -> None:
    user_id = update.effective_user.id
    user = User[user_id]
    user.update_subscription()
    update.message.reply_text(
        BOT_SUBSCRIBED_USR if user.subscribed else BOT_UNSUBSCRIBED_USR,
        reply_markup=get_keyboard(update)
    )
