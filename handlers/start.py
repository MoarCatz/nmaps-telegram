from telegram import Bot, Update
from telegram.ext import MessageHandler, Filters, RegexHandler

from bot.helpers import get_keyboard, private
from bot.phrases import (
    MENU_ROADS,
    BOT_PRIVATE_ROAD_REPORT_USR,
    BOT_INLINE_INSTRUCTIONS,
    BOT_ACTION_SELECT,
    BOT_UNRECOGNIZED_MESSAGE,
)


@private
def send_instructions(_bot: Bot, update: Update, start=False) -> None:
    instructions = {
        MENU_ROADS: BOT_PRIVATE_ROAD_REPORT_USR,
        "/start inline-help": BOT_INLINE_INSTRUCTIONS,
        "/start": BOT_ACTION_SELECT,
    }
    if update.message.text in instructions:
        text = instructions[update.message.text]
    elif start:
        text = BOT_ACTION_SELECT
    else:
        text = BOT_UNRECOGNIZED_MESSAGE
    update.message.reply_markdown(text, reply_markup=get_keyboard(update))


start_handler = MessageHandler(Filters.private, send_instructions)
roads_instructions_handler = RegexHandler(
    fr"(/start[a-z-]*|{MENU_ROADS})", send_instructions
)
