from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Job, JobQueue

from config import nmaps_chat, mods_chat, roads_chat, english_chat
from phrases import (BOT_WELCOME_MODS, BOT_WELCOME_ROADS, BOT_WELCOME_ENG,
                     BOT_WELCOME_NMAPS, BTN_NOT_BOT, BOT_NOT_VERIFIED,
                     BOT_VERIFIED)

VERIFY_MARKUP = InlineKeyboardMarkup(
    [[InlineKeyboardButton(BTN_NOT_BOT, callback_data='not_bot')]])


def welcome(bot: Bot, update: Update, job_queue: JobQueue) -> None:
    user_name = update.effective_message.new_chat_members[0].name
    user_id = update.effective_message.new_chat_members[0].id
    to_welcome, chat, message = False, 0, ''

    if update.effective_chat.id == nmaps_chat:
        bot.delete_message(nmaps_chat,
                           update.effective_message.message_id)

        msg = bot.send_message(nmaps_chat,
                               BOT_WELCOME_NMAPS.format(user_name),
                               reply_markup=VERIFY_MARKUP,
                               parse_mode='html')
        bot.restrict_chat_member(nmaps_chat, user_id, can_send_messages=False)
        job_queue.run_once(kick_and_delete_message,
                           300,
                           {'user_id': user_id,
                            'msg_id': msg.message_id,
                            'chat_id': nmaps_chat},
                           str(user_id))
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


def verify_user(bot: Bot, update: Update, job_queue: JobQueue):
    query_user_id = update.callback_query.from_user.id
    jobs = job_queue.get_jobs_by_name(str(update.effective_user.id))
    if not jobs:
        bot.answer_callback_query(update.callback_query.id,
                                  text=BOT_NOT_VERIFIED)
        return
    job = jobs[0]
    data = job.context
    if query_user_id == data['user_id']:
        job.schedule_removal()
        bot.delete_message(data['chat_id'], data['msg_id'])
        bot.restrict_chat_member(data['chat_id'],
                                 data['user_id'],
                                 can_send_messages=True,
                                 can_add_web_page_previews=True,
                                 can_send_media_messages=True,
                                 can_send_other_messages=True)
        bot.answer_callback_query(update.callback_query.id,
                                  text=BOT_VERIFIED)


def kick_and_delete_message(bot: Bot, job: Job):
    data = job.context
    bot.delete_message(data['chat_id'], data['msg_id'])
    bot.kick_chat_member(data['chat_id'], data['user_id'])
