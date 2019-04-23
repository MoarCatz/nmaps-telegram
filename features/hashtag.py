from telegram import Bot, Update, Message

from features.roads import new_roadblock
from features.screenshot import screenshot

tags = {'#скрин': screenshot,
        '#screen': screenshot,
        '#перекрытие': new_roadblock,
        '#roadblock': new_roadblock,
        '#дороги': new_roadblock,
        '#roads': new_roadblock}


def hashtag(bot: Bot, update: Update):
    message = update.message
    entities = {message.parse_caption_entity(entity) for entity
                in message.parse_caption_entities(types='hashtag')}
    entities.update({message.parse_entity(entity) for entity
                     in message.parse_entities(types='hashtag')})

    for entity in entities:
        if entity in tags:
            tags[entity](bot, extract_reply(message))


def extract_reply(message: Message) -> Message:
    return message.reply_to_message if message.reply_to_message else message
