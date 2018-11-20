from cloudinary.uploader import upload
from telegram import Bot, Message, ChatAction

from features.capturer import Capturer, IllegalURL
from features.devmode import enable_dev
from phrases import BOT_ILLEGAL_URL


if not enable_dev():
    cpt = Capturer()


def screenshot(bot: Bot, message: Message) -> None:
    for entity in message.parse_entities():
        if entity.type == 'url':
            url = message.parse_entity(entity)
            try:
                bot.send_chat_action(message.chat_id,
                                     ChatAction.UPLOAD_PHOTO)
                scrn = cpt.take_screenshot(url)
                scrn_url = upload(scrn)['secure_url']
                bot.send_photo(message.chat_id, scrn_url)
            except IllegalURL:
                message.reply_text(BOT_ILLEGAL_URL)
