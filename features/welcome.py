from telegram import Bot, Update

from config import nmaps_chat, mods_chat, roads_chat, english_chat
from phrases import BOT_WELCOME_NMAPS, BOT_WELCOME_MODS, BOT_WELCOME_ROADS, BOT_WELCOME_ENG


def welcome(bot: Bot, update: Update) -> None:
    user_name = update.effective_message.new_chat_members[0].name
    to_welcome, chat, message = False, 0, ''

    if update.effective_chat.id == nmaps_chat:
        pass
        '''to_welcome = True
        chat = nmaps_chat
        message = BOT_WELCOME_NMAPS.format(user_name)'''
    elif update.effective_chat.id == mods_chat:
        to_welcome = True
        chat = mods_chat
        message = BOT_WELCOME_MODS.format(user_name)
    elif update.effective_chat.id == roads_chat:
        to_welcome = True
        chat = roads_chat
        message = BOT_WELCOME_ROADS.format(user_name)
    elif update.effective_chat.id == english_chat:
        to_welcome = True
        chat = english_chat
        message = BOT_WELCOME_ENG.format(user_name)

    if to_welcome:
        bot.send_message(chat,
                         message,
                         reply_to_message_id=update.message.message_id,
                         disable_web_page_preview=True)
