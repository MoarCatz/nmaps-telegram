from cloudinary.uploader import upload
from telegram import Bot, Update, ChatAction

from features.capturer import Capturer, IllegalURL
from phrases import BOT_ILLEGAL_URL

cpt = Capturer()


def screenshot(bot: Bot, update: Update) -> None:
    for entity in update.message['entities']:
        if entity['type'] == 'url':
            url_start = int(entity['offset'])
            url_end = url_start + int(entity['length'])
            try:
                bot.send_chat_action(update.effective_chat.id,
                                     ChatAction.UPLOAD_PHOTO)
                scrn = cpt.take_screenshot(
                    update.message.text[url_start:url_end]
                )
                scrn_url = upload(scrn)['secure_url']
                bot.send_photo(update.message.chat.id, scrn_url)
            except IllegalURL:
                update.message.reply_text(BOT_ILLEGAL_URL)
