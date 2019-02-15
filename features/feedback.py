from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from config import FEEDBACK_REQUESTED, alexfox
from features.wrappers import private
from helpers import get_keyboard
from phrases import BOT_SEND_FEEDBACK_USR, MENU_RETURN, \
    BOT_FEEDBACK_SENT_USR, BOT_DELIVER_FEEDBACK


@private
def request_feedback(_bot: Bot, update: Update) -> int:
    update.message.reply_text(
        BOT_SEND_FEEDBACK_USR,
        reply_markup=ReplyKeyboardMarkup([[MENU_RETURN]],
                                         one_time_keyboard=True,
                                         resize_keyboard=True))
    return FEEDBACK_REQUESTED


def receive_feedback(bot: Bot, update: Update) -> int:
    update.message.reply_text(
        BOT_FEEDBACK_SENT_USR,
        reply_markup=get_keyboard(update))
    bot.send_message(alexfox,
                     BOT_DELIVER_FEEDBACK.format(update.effective_user.name,
                                                 update.message.text),
                     parse_mode='markdown')
    return ConversationHandler.END
