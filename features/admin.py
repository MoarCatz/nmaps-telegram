from pony.orm import count, db_session
from telegram import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                      InlineKeyboardButton)
from telegram.bot import Bot, Update

from config import admin_menu as menu
from db import Chat
from phrases import (BOT_ADMIN_MENU, BOT_CHATS_MANAGE, BTN_NEXT_PAGE,
                     BTN_PREV_PAGE, MENU_RETURN, BOT_SAVED)
from .subscription import subscribe_chat, unsubscribe_chat
from .wrappers import admins_only, private


@private
@admins_only
def admin_menu(bot: Bot, update: Update) -> None:
    bot.send_message(
        update.effective_chat.id,
        BOT_ADMIN_MENU,
        reply_markup=ReplyKeyboardMarkup(menu,
                                         one_time_keyboard=True,
                                         resize_keyboard=True))


@private
@admins_only
def chats_management(_: Bot, update: Update) -> None:
    update.message.reply_markdown(
        BOT_CHATS_MANAGE,
        reply_markup=InlineKeyboardMarkup(get_chats_keyboard(1)))


def update_chat_subscription(bot: Bot, update: Update) -> None:
    query = update.callback_query
    chat_id = int(query.data.split('_')[-2])
    page = int(query.data.split('_')[-1])
    if query.data.startswith('chats_subscribe'):
        subscribe_chat(chat_id)
    else:
        unsubscribe_chat(chat_id)
    bot.edit_message_reply_markup(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=InlineKeyboardMarkup(get_chats_keyboard(page)))
    query.answer(BOT_SAVED)


def change_chats_page(bot: Bot, update: Update) -> None:
    query = update.callback_query
    page = int(query.data.split('-')[1])
    bot.edit_message_reply_markup(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=InlineKeyboardMarkup(get_chats_keyboard(page)))


@db_session
def get_chats_keyboard(page: int):
    chats = Chat.select().order_by(Chat.id).page(page)
    keyboard = []
    for chat in chats:
        if chat.is_subscribed():
            data = 'chats_unsubscribe_{}_{}'.format(chat.chat_id, page)
            text = '🔔 {}'
        else:
            data = 'chats_subscribe_{}_{}'.format(chat.chat_id, page)
            text = '🔕 {}'
        keyboard.append([InlineKeyboardButton(text.format(chat.name),
                                              callback_data=data)])
    footer = []
    if page > 1:
        footer.append(InlineKeyboardButton(
            BTN_PREV_PAGE,
            callback_data='chats_{}'.format(page - 1)))
    footer.append(InlineKeyboardButton(
        MENU_RETURN,
        callback_data='admin_return'))
    if count(c for c in Chat) > page * 10:
        footer.append(InlineKeyboardButton(
            BTN_NEXT_PAGE,
            callback_data='chats_{}'.format(page + 1)))
    keyboard.append(footer)
    return keyboard
