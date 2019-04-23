import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from bot.config import SEARCH_QUERY_REQUESTED, rules_search_url, club_search_url
from bot.helpers import private
from bot.phrases import (MENU_SEARCH_RULES, BOT_SRCH_QUERY, MENU_RETURN,
                         BOT_UNEXPECTED_ERROR, BOT_NOT_FOUND, BOT_SRCH_CONTINUE)
from features.start import send_instructions


@private
def search(_bot: Bot, update: Update, user_data: dict) -> int:
    if update.message.text == MENU_SEARCH_RULES:
        user_data['search'] = 'rules'
    else:
        user_data['search'] = 'club'
    update.message.reply_text(
        BOT_SRCH_QUERY,
        reply_markup=ReplyKeyboardMarkup([[MENU_RETURN]],
                                         resize_keyboard=True,
                                         one_time_keyboard=True)
    )
    return SEARCH_QUERY_REQUESTED


def run_search(bot: Bot, update: Update, user_data: dict) -> int:
    if 'search' not in user_data:
        update.message.reply_text(BOT_UNEXPECTED_ERROR)
        send_instructions(bot, update, start=True)
        return ConversationHandler.END
    if user_data['search'] == 'rules':
        retrieve_search_results(update, in_rules=True)
    elif user_data['search'] == 'club':
        retrieve_search_results(update, in_rules=False)

    return SEARCH_QUERY_REQUESTED


def retrieve_search_results(update: Update, in_rules: bool) -> None:
    if in_rules:
        page = requests.get(rules_search_url +
                            update.message.text.replace(' ', '+'))
    else:
        page = requests.get(club_search_url +
                            update.message.text.replace(' ', '+'))
    soup = BeautifulSoup(page.text, 'lxml')
    answer = ''

    if in_rules:
        for item in soup.find_all('div', class_='results__item'):
            if not item.attrs['data-document'].startswith('/support/nmaps/'):
                continue
            title = item.find('div', class_='results__title').text
            link = 'https://yandex.ru' + item.attrs['data-document']
            text = item.find('div', class_='results__text').text
            answer += '[' + title + '](' + link + ')\n```' \
                      + text + '```\n____________________\n'
    else:
        for item in soup.find_all('a', class_='b-serp-item'):
            title = item.find('h2').text
            link = 'https://yandex.ru' + item['href']
            answer += '[' + title + '](' + link + ')\n____________________\n'

    if not answer:
        update.message.reply_text(BOT_NOT_FOUND)
    else:
        update.message.reply_markdown(answer,
                                      disable_web_page_preview=True)
    update.message.reply_text(
        BOT_SRCH_CONTINUE,
        reply_markup=ReplyKeyboardMarkup([[MENU_RETURN]],
                                         resize_keyboard=True,
                                         one_time_keyboard=True))
