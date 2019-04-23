from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton

from bot.config import bookmarks
from bot.helpers import private
from bot.phrases import BOT_CHS_LINK
from features.start import send_instructions


@private
def send_bookmarks(bot: Bot, update: Update):
    keyboard = [[InlineKeyboardButton(title, url=url)
                 for title, url in row] for row in bookmarks]
    update.message.reply_text(BOT_CHS_LINK,
                              reply_markup=InlineKeyboardMarkup(keyboard))
    send_instructions(bot, update, True)
