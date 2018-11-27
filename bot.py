import logging

from telegram import Bot, Update, ChatAction
from telegram.error import TimedOut
from telegram.ext import Updater, MessageHandler, RegexHandler, Filters, \
    InlineQueryHandler, ConversationHandler, CallbackQueryHandler

from config import *
from features.bookmarks import bookmarks
from features.devmode import enable_dev
from features.feedback import request_feedback, receive_feedback
from features.hashtag import hashtag
from features.inline import inline_search
from features.roads import roadblock_callback
from features.rss import rss
from features.search import search, run_search
from features.subscription import update_subscription, subscribed
from features.transliterator import transliterate, retrieve_transliteration
from features.welcome import welcome, verify_user
from features.wrappers import private
from helpers import get_keyboard
from phrases import *
from start import send_instructions

# Enable logging
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [bot]\n%(message)s',
                    datefmt='%d-%m %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


@private
def cancel(_bot: Bot, update: Update, user_data: dict) -> int:
    update.message.reply_text(
        BOT_CANCELLED,
        reply_markup=get_keyboard(update,
                                  subscribed(update.message.from_user.id)))
    user_data.clear()
    return ConversationHandler.END


def error(_bot: Bot, _update: Update, exc: Exception) -> None:
    if exc == TimedOut or exc == 'Invalid server response':
        return
    logger.error(exc)


@private
def typing(bot: Bot, update: Update) -> None:
    bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)


def main():
    """Start the bot"""
    updater = Updater(telegram_key)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    jobs = updater.job_queue

    # Typing
    dp.add_handler(MessageHandler(Filters.all, typing), group=-1)

    # Welcome
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                  welcome, pass_job_queue=True))

    dp.add_handler(RegexHandler(r'(/start[a-z-]*|{})'.format(MENU_ROADS),
                                send_instructions))
    dp.add_handler(RegexHandler(MENU_LINKS, bookmarks))
    dp.add_handler(MessageHandler((Filters.entity('hashtag') |
                                   Filters.caption_entity('hashtag')),
                                  hashtag))
    dp.add_handler(RegexHandler(r'({}|{})'.format(MENU_SUBSCRIBE,
                                                  MENU_UNSUBSCRIBE),
                                update_subscription))

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

    # This one will handle any random message
    dp.add_handler(MessageHandler(Filters.all, send_instructions))

    # Logging errors
    dp.add_error_handler(error)

    # Adds repeating jobs
    if not enable_dev():
        jobs.run_repeating(rss, 300)

    # Inline handler
    dp.add_handler(InlineQueryHandler(inline_search))

    # Actually start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
