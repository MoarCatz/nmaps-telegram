from telegram import Bot, Update

from helpers import get_keyboard
from phrases import MENU_ROADS, BOT_PRIVATE_ROAD_REPORT_USR, \
    BOT_INLINE_INSTRUCTIONS, BOT_ACTION_SELECT, BOT_UNRECOGNIZED_MESSAGE


def send_instructions(_bot: Bot, update: Update, start=False) -> None:
    instructions = {MENU_ROADS: BOT_PRIVATE_ROAD_REPORT_USR,
                    '/start inline-help': BOT_INLINE_INSTRUCTIONS,
                    '/start': BOT_ACTION_SELECT}
    if update.message.text in instructions:
        text = instructions[update.message.text]
    elif start:
        text = BOT_ACTION_SELECT
    else:
        text = BOT_UNRECOGNIZED_MESSAGE
    update.message.reply_markdown(
        text,
        reply_markup=get_keyboard(update))
