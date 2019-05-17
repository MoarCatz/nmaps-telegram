from handlers.admin import (
    admin_return_handler,
    admin_menu_handler,
    chats_management_handler,
    chats_page_handler,
    chats_subscriptions_handler,
)
from handlers.bookmarks import bookmarks_handler
from handlers.cancel import cancel_handler
from handlers.checkin import checkin_handler
from handlers.feedback import feedback_handler
from handlers.hashtag import hashtag_handler
from handlers.roads import roadblock_callback_handler
from handlers.inline import inline_search_handler
from handlers.search import search_handler
from handlers.start import start_handler, roads_instructions_handler
from handlers.subscription import subscription_handler
from handlers.transliterator import transliterator_handler
from handlers.welcome import verification_handler, welcome_handler

handlers = [bookmarks_handler, transliterator_handler, search_handler,
            subscription_handler, feedback_handler,
            start_handler,
            admin_return_handler,
            admin_menu_handler,
            chats_management_handler,
            chats_page_handler, chats_subscriptions_handler,
            cancel_handler, hashtag_handler,
            roadblock_callback_handler, inline_search_handler,
            roads_instructions_handler,
            verification_handler, welcome_handler]
