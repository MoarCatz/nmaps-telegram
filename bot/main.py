from telegram.ext import (Updater, MessageHandler, RegexHandler, Filters,
                          InlineQueryHandler, ConversationHandler,
                          CallbackQueryHandler)

from bot.config import *
from bot.devmode import enable_dev, get_headers
from bot.helpers import cancel
from bot.logger import error
from bot.phrases import *
from bot.service import init_db
from features.admin import (admin_menu, chats_management, change_chats_page,
                            update_chat_subscription)
from features.bookmarks import bookmarks
from features.checkin import add_user, add_chat
from features.feedback import request_feedback, receive_feedback
from features.hashtag import hashtag
from features.inline import inline_search
from features.roads import roadblock_callback
from features.rss import rss
from features.search import search, run_search
from features.start import send_instructions
from features.subscription import update_subscription
from features.transliterator import transliterate, retrieve_transliteration
from features.welcome import welcome, verify_user

# Setup
updater = Updater(telegram_key, request_kwargs=get_headers())
dp = updater.dispatcher
jobs = updater.job_queue

# Welcome
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                              welcome, pass_job_queue=True))

dp.add_handler(RegexHandler(fr'(/start[a-z-]*|{MENU_ROADS})',
                            send_instructions))
dp.add_handler(RegexHandler(MENU_LINKS, bookmarks))
dp.add_handler(MessageHandler((Filters.entity('hashtag') |
                               Filters.caption_entity('hashtag')),
                              hashtag))
dp.add_handler(RegexHandler(MENU_ADMIN, admin_menu))
dp.add_handler(RegexHandler(MENU_CHATS, chats_management))
dp.add_handler(RegexHandler(fr'({MENU_SUBSCRIBE}|{MENU_UNSUBSCRIBE})',
                            update_subscription))
dp.add_handler(RegexHandler(MENU_RETURN, cancel, pass_user_data=True))

# Conversations
dp.add_handler(ConversationHandler(
    entry_points=[RegexHandler(MENU_FEEDBACK, request_feedback)],
    states={
        FEEDBACK_REQUESTED: [RegexHandler(r'^(?!⬅ Вернуться)',
                                          receive_feedback)]
    },
    fallbacks=[RegexHandler(MENU_RETURN,
                            cancel,
                            pass_user_data=True)]
))
dp.add_handler(ConversationHandler(
    entry_points=[RegexHandler(MENU_SEARCH_CLUB,
                               search,
                               pass_user_data=True),
                  RegexHandler(MENU_SEARCH_RULES,
                               search,
                               pass_user_data=True)],
    states={
        SEARCH_QUERY_REQUESTED: [RegexHandler(r'^(?!⬅ Вернуться)',
                                              run_search,
                                              pass_user_data=True)]
    },
    fallbacks=[RegexHandler(MENU_RETURN,
                            cancel,
                            pass_user_data=True)]
))
dp.add_handler(ConversationHandler(
    entry_points=[RegexHandler(MENU_TRANSLIT,
                               transliterate)],
    states={
        TRANSLITERATE_REQUESTED: [RegexHandler(r'^(?!⬅ Вернуться)',
                                               retrieve_transliteration)]
    },
    fallbacks=[RegexHandler(MENU_RETURN,
                            cancel,
                            pass_user_data=True)]
))

# Callbacks
dp.add_handler(CallbackQueryHandler(roadblock_callback,
                                    pattern=r'^road\w+'))
dp.add_handler(CallbackQueryHandler(verify_user,
                                    pattern=r'not_bot',
                                    pass_job_queue=True))
dp.add_handler(CallbackQueryHandler(change_chats_page,
                                    pattern=r'chats_\d+'))
dp.add_handler(CallbackQueryHandler(update_chat_subscription,
                                    pattern=r'chats_\D+'))
dp.add_handler(CallbackQueryHandler(admin_menu,
                                    pattern=r'admin_return'))

# This one will handle any random message
dp.add_handler(MessageHandler(Filters.private, send_instructions))

# Checkin
dp.add_handler(MessageHandler(Filters.private, add_user), group=1)
dp.add_handler(MessageHandler(Filters.group, add_chat), group=1)

# Logging errors
dp.add_error_handler(error)

# Adds repeating jobs
if not enable_dev():
    jobs.run_repeating(rss, 300)

# Inline handler
dp.add_handler(InlineQueryHandler(inline_search))


if __name__ == '__main__':
    init_db()

    # Actually start the bot
    updater.start_polling()
    updater.idle()
