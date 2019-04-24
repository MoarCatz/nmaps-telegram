from telegram import Bot, Update
from telegram.ext import MessageHandler, Filters

from bot.helpers import get_original_message
from handlers.roads import new_roadblock

tags = {
    "#перекрытие": new_roadblock,
    "#roadblock": new_roadblock,
    "#дороги": new_roadblock,
    "#roads": new_roadblock,
}


def hashtag(bot: Bot, update: Update):
    message = update.message
    entities = {
        message.parse_caption_entity(entity)
        for entity in message.parse_caption_entities(types="hashtag")
    }
    entities.update(
        {
            message.parse_entity(entity)
            for entity in message.parse_entities(types="hashtag")
        }
    )

    for entity in entities:
        if entity in tags:
            tags[entity](bot, get_original_message(message))


hashtag_handler = MessageHandler(
    (Filters.entity("hashtag") | Filters.caption_entity("hashtag")), hashtag
)
