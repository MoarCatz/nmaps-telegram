from typing import Any

from pony.orm import db_session
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Bot,
    Update,
    Message,
    CallbackQuery,
    User,
    ParseMode
)
from telegram.ext import BaseFilter, CallbackQueryHandler

from bot.config import mods_chat, roads_chat, roads_staff, road_hashtag
from bot.models import Roadblock, User as U
from bot.phrases import *


class RoadblockHashtagHandler(BaseFilter):
    def filter(self, message: Message) -> Any:
        if not message.caption:
            return False
        return road_hashtag.match(message.caption)


roadblock_filter = RoadblockHashtagHandler()


def build_keyboard(buttons: tuple) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(label, callback_data=callback)]
            for label, callback in buttons
        ]
    )


staff_buttons = (
    (BTN_ROADS_CLOSED, "road_closed"),
    (BTN_ROADS_OPENED, "road_opened"),
    (BTN_ROADS_INFOPOINT, "road_info_added"),
    (BTN_CANCEL, "road_cancel"),
)

mods_buttons = (
    (BTN_ROADS_ACCEPT, "road_mod_approve"),
    (BTN_CANCEL, "road_cancel"),
    (BTN_ROADS_REQUEST_INFO, "road_mod_request_info"),
    (BTN_ROADS_FRAUD, "road_mod_ban"),
)

investigation_buttons = (
    (BTN_ROADS_ACCEPT, "road_mod_approve"),
    (BTN_CANCEL, "road_cancel"),
)

staff_keyboard, mods_keyboard, investigation_keyboard = map(
    build_keyboard, (staff_buttons, mods_buttons, investigation_buttons)
)


def new_roadblock(bot: Bot, message: Message) -> None:
    if banned(message.from_user) or message.chat_id == roads_chat:
        return

    user_id = message.from_user.id
    user = bot.get_chat_member(mods_chat, user_id)
    if user["status"] in ("creator", "administrator", "member"):
        bypass_moderators(bot, message)
        return

    message.reply_markdown(BOT_MSG_ACCEPT.format(
        message.from_user.mention_markdown()))
    msg = BOT_REQUEST_CHECK.format(message.from_user.name)
    mods_message = bot.send_message(mods_chat, msg, reply_markup=mods_keyboard)
    message.forward(mods_chat)

    with db_session:
        Roadblock(
            author=message.from_user.id,
            chat_id=message.chat_id,
            chat_message_id=message.message_id,
            mods_message_id=mods_message.message_id,
        )


def cancel_roadblock(bot: Bot, query: CallbackQuery) -> None:
    if query.message.chat.id == mods_chat:
        nmaps_message = retrieve_roadblock(mods_id=query.message.message_id)
    else:
        if query.from_user.last_name not in roads_staff:
            query.answer(BOT_NOT_ROAD_STAFF)
            return
        nmaps_message = retrieve_roadblock(roads_id=query.message.message_id)
    bot.send_message(
        nmaps_message.chat_id,
        BOT_REQUEST_CANCELLED_USR,
        reply_to_message_id=nmaps_message.chat_message_id,
    )
    query.edit_message_text(
        BOT_REQUEST_CANCELLED.format(
            query.from_user.mention_markdown()
        ),
        parse_mode=ParseMode.MARKDOWN
    )


def ban_roadblock_author(_bot: Bot, query: CallbackQuery) -> None:
    if query.message.chat.id == mods_chat:
        nmaps_message = retrieve_roadblock(mods_id=query.message.message_id)
    else:
        nmaps_message = retrieve_roadblock(roads_id=query.message.message_id)
    query.edit_message_text(
        BOT_USER_BANNED.format(query.from_user.mention_markdown()),
        parse_mode=ParseMode.MARKDOWN,
    )
    with db_session:
        U.get(id=nmaps_message.author.id).banned = True


def request_roadblock_info(_bot: Bot, query: CallbackQuery) -> None:
    query.edit_message_text(
        BOT_INVESTIGATING.format(query.from_user.mention_markdown()),
        reply_markup=investigation_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )


def accept_roadblock(bot: Bot, query: CallbackQuery) -> None:
    query.edit_message_text(
        BOT_SENT_TO_STAFF.format(query.from_user.mention_markdown()),
        parse_mode=ParseMode.MARKDOWN,
    )
    nmaps_message = retrieve_roadblock(mods_id=query.message.message_id)
    bot.forward_message(
        roads_chat, nmaps_message.chat_id, nmaps_message.chat_message_id
    )
    roads_message = bot.send_message(
        roads_chat, BOT_NEW_ROADBLOCK, reply_markup=staff_keyboard
    )

    nmaps_message = retrieve_roadblock(mods_id=query.message.message_id)

    with db_session:
        Roadblock.get(
            chat_message_id=nmaps_message.chat_message_id
        ).roads_message_id = roads_message.message_id


def bypass_moderators(bot: Bot, message: Message) -> None:
    message.reply_markdown(BOT_MSG_ACCEPT.format(
        message.from_user.mention_markdown()))
    bot.forward_message(roads_chat, message.chat_id, message.message_id)
    roads_message = bot.send_message(
        roads_chat, BOT_NEW_ROADBLOCK, reply_markup=staff_keyboard
    )

    with db_session:
        Roadblock(
            author=message.from_user.id,
            chat_id=message.chat_id,
            chat_message_id=message.message_id,
            roads_message_id=roads_message.message_id,
        )


def send_roadblock_resolution(bot: Bot, query: CallbackQuery) -> None:
    if query.from_user.last_name not in roads_staff:
        query.answer(BOT_NOT_ROAD_STAFF)
        return

    nmaps_message = retrieve_roadblock(roads_id=query.message.message_id)

    if query.data == "road_closed":
        msg = BOT_ROADBLOCK_SET_USR
        btn_msg = BOT_ROADBLOCK_SET
    elif query.data == "road_opened":
        msg = BOT_ROADBLOCK_DEL_USR
        btn_msg = BOT_ROADBLOCK_DEL
    else:
        msg = BOT_INFOPOINT_SET_USR
        btn_msg = BOT_INFOPOINT_SET

    bot.send_message(
        nmaps_message.chat_id, msg,
        reply_to_message_id=nmaps_message.chat_message_id
    )
    query.edit_message_text(
        btn_msg.format(query.from_user.mention_markdown()),
        parse_mode=ParseMode.MARKDOWN
    )


@db_session
def retrieve_roadblock(**kwargs) -> Roadblock:
    if "mods_id" in kwargs:
        return Roadblock.get(mods_message_id=kwargs["mods_id"])
    else:
        return Roadblock.get(roads_message_id=kwargs["roads_id"])


def roadblock_callback(bot: Bot, update: Update) -> None:
    query = update.callback_query
    if query.data == "road_mod_approve":
        accept_roadblock(bot, update.callback_query)
    elif query.data == "road_cancel":
        cancel_roadblock(bot, update.callback_query)
    elif query.data == "road_mod_request_info":
        request_roadblock_info(bot, query)
    elif query.data == "road_mod_ban":
        ban_roadblock_author(bot, update.callback_query)
    else:
        send_roadblock_resolution(bot, update.callback_query)


@db_session
def banned(user: User) -> bool:
    return U.get(id=user.id).banned


roadblock_callback_handler = CallbackQueryHandler(
    roadblock_callback, pattern=r"^road\w+"
)
