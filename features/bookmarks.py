from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup

from bot.helpers import private
from bot.phrases import STREET_TRANSLITERATOR, BOT_CHS_LINK
from features.start import send_instructions


@private
def bookmarks(bot: Bot, update: Update) -> None:
    keyboard = [
        [
            InlineKeyboardButton(
                'Правила',
                url='https://yandex.ru/support/nmaps/rules_2.html'
            ),
            InlineKeyboardButton(
                'Клуб',
                url='https://yandex.ru/blog/narod-karta'
            )
        ],
        [
            InlineKeyboardButton('ПКК', url='https://pkk5.rosreestr.ru/'),
            InlineKeyboardButton('ФИАС', url='https://fias.nalog.ru/')
        ],
        [
            InlineKeyboardButton('ЕГРП365', url='https://egrp365.ru/map/'),
            InlineKeyboardButton('TerraServer',
                                 url='https://www.terraserver.com/')
        ],
        [
            InlineKeyboardButton('Реформа ЖКХ',
                                 url='https://www.reformagkh.ru/'),
            InlineKeyboardButton('КЛАДР',
                                 url='https://kladr-rf.ru/')
        ],
        [
            InlineKeyboardButton('Водный реестр',
                                 url='http://textual.ru/gvr'),
            InlineKeyboardButton('ФГИС ТП',
                                 url='http://fgis.economy.gov.ru/fgis/')
        ],
        [
            InlineKeyboardButton('Транслитератор названий',
                                 url=STREET_TRANSLITERATOR),
            InlineKeyboardButton('Подбор слов',
                                 url='https://wordstat.yandex.ru')
        ],
        [
            InlineKeyboardButton('FAQ НЯК',
                                 url='https://tinyurl.com/FAQ-NYK')
        ]
    ]
    update.message.reply_text(BOT_CHS_LINK,
                              reply_markup=InlineKeyboardMarkup(keyboard))
    send_instructions(bot, update, True)
