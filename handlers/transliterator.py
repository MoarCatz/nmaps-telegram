import urllib.parse
import urllib.request

from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, RegexHandler

from bot.config import TRANSLITERATE_REQUESTED, transliterator
from handlers import cancel_handler
from bot.helpers import private
from bot.phrases import (
    BOT_TRANSLITERATE_QUERY,
    MENU_RETURN,
    BOT_TRANS_CONTINUE,
    MENU_TRANSLIT,
)


@private
def transliterate(_bot: Bot, update: Update) -> int:
    update.message.reply_markdown(
        BOT_TRANSLITERATE_QUERY,
        reply_markup=ReplyKeyboardMarkup(
            [[MENU_RETURN]], resize_keyboard=True, one_time_keyboard=True
        ),
        disable_web_page_preview=True,
    )
    return TRANSLITERATE_REQUESTED


def retrieve_transliteration(_bot: Bot, update: Update) -> int:
    update.message.reply_text(
        urllib.request.urlopen(transliterator + urllib.parse.quote(update.message.text))
        .read()
        .decode()
        .strip('"')
    )
    update.message.reply_text(
        BOT_TRANS_CONTINUE,
        reply_markup=ReplyKeyboardMarkup(
            [[MENU_RETURN]], resize_keyboard=True, one_time_keyboard=True
        ),
    )
    return TRANSLITERATE_REQUESTED


transliterator_handler = ConversationHandler(
    entry_points=[RegexHandler(MENU_TRANSLIT, transliterate)],
    states={
        TRANSLITERATE_REQUESTED: [
            RegexHandler(r"^(?!⬅ Вернуться)", retrieve_transliteration)
        ]
    },
    fallbacks=[cancel_handler],
)
