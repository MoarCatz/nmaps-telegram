from telegram import Bot, Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler, RegexHandler

from bot.config import FEEDBACK_REQUESTED, alexfox
from handlers import cancel_handler
from bot.helpers import get_keyboard, private
from bot.phrases import (
    BOT_SEND_FEEDBACK_USR,
    MENU_FEEDBACK,
    MENU_RETURN,
    BOT_FEEDBACK_SENT_USR,
    BOT_DELIVER_FEEDBACK,
)


@private
def request_feedback(_bot: Bot, update: Update) -> int:
    update.message.reply_text(
        BOT_SEND_FEEDBACK_USR,
        reply_markup=ReplyKeyboardMarkup(
            [[MENU_RETURN]], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return FEEDBACK_REQUESTED


def receive_feedback(bot: Bot, update: Update) -> int:
    update.message.reply_text(BOT_FEEDBACK_SENT_USR,
                              reply_markup=get_keyboard(update))
    bot.send_message(
        alexfox,
        BOT_DELIVER_FEEDBACK.format(update.effective_user.name,
                                    update.message.text),
        parse_mode=ParseMode.MARKDOWN,
    )
    return ConversationHandler.END


feedback_handler = ConversationHandler(
    entry_points=[RegexHandler(MENU_FEEDBACK, request_feedback)],
    states={FEEDBACK_REQUESTED: [RegexHandler(r"^(?!⬅ Вернуться)",
                                              receive_feedback)]},
    fallbacks=[cancel_handler],
)
