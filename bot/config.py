import os
import re

from algoliasearch.search_client import SearchClient

from bot.phrases import *

# The main bot token
telegram_key = os.getenv('TELEGRAM_API_KEY',
                         '331488080:AAH8PEA9WnsZtFubYnwFI5EWDq1fvqb9ZAE')
# -----------------
# Database credentials
db_creds = {'host': os.getenv('DBHOST', 'localhost'),
            'database': os.getenv('DBNAME', 'postgres'),
            'user': os.getenv('DBUSER', 'postgres'),
            'password': os.getenv('DBPASS', 'postgres')}
# -----------------
# Inline search tool
client = SearchClient.create(os.getenv('ALGOLIA_CLIENT', 'key'),
                             os.getenv('ALGOLIASEARCH_API_KEY_SEARCH', 'key'))
# Algolia indices
links = client.init_index('links')
rules = client.init_index('rules')
rubrics = client.init_index('rubrics')
indices = (links, rules, rubrics)
# -----------------
# Hashtags
screen_hashtags = re.compile(f'.*#({HASH_SCREEN}|{HASH_SCREEN_ENG}).*',
                             flags=re.S | re.I)
road_hashtag = re.compile(f'.*#({HASH_ROADBLOCK}|{HASH_ROADBLOCK_ENG}|{HASH_ROAD}|{HASH_ROAD_ENG}).*',
                          flags=re.S | re.I)
# -----------------
FEEDBACK_REQUESTED, SEARCH_QUERY_REQUESTED, TRANSLITERATE_REQUESTED = 1, 1, 1
# -----------------
# Menu buttons
main_menu = [[MENU_LINKS],
             [MENU_TRANSLIT],
             [MENU_SEARCH_CLUB, MENU_SEARCH_RULES],
             [MENU_ROADS, MENU_FEEDBACK]]

admin_menu = [[MENU_CHATS],
              [MENU_RETURN]]
# -----------------
# Chats ids'
nmaps_chat = int(os.getenv('NMAPSCHAT', '-1001136617457'))
mods_chat = int(os.getenv('MODSCHAT', '-1001304260305'))
roads_chat = int(os.getenv('ROADSCHAT', '-259382209'))
english_chat = -1001308645324
# -----------------
# Admins ids'
alexfox = 30375360
bforest = 291582989
admins = list(map(int, os.getenv('ADMINS',
                                 f'{alexfox},{bforest}').split(',')))
roads_staff = os.getenv('ROADS_STAFF', 'Bagirov').split(',')
# -----------------
# Used links
instantview_url = 'https://t.me/iv?url={}&rhash=082e533d0deed1'
rules_search_url = 'https://yandex.ru/support/search-results/?service=nmaps&query='
club_search_url = 'https://yandex.ru/blog/narod-karta/search?text='
transliterator = 'https://script.google.com/macros/s/AKfycbwCfGxk22dNUACxjRMULtVo4UzzRwfk49g9rIy-yycPMACtEps2/exec?'
# -----------------
# Bookmarks
bookmarks = (
        (
            ('Правила', 'https://yandex.ru/support/nmaps/rules_2.html'),
            ('Клуб', 'https://yandex.ru/blog/narod-karta')
        ),
        (
            ('ПКК', 'https://pkk5.rosreestr.ru/'),
            ('ФИАС', 'https://fias.nalog.ru/')
        ),
        (
            ('ЕГРП365', 'https://egrp365.ru/map/'),
            ('TerraServer', 'https://www.terraserver.com/')
        ),
        (
            ('Реформа ЖКХ', 'https://www.reformagkh.ru/'),
            ('КЛАДР', 'https://kladr-rf.ru/')
        ),
        (
            ('Водный реестр', 'http://textual.ru/gvr'),
            ('ФГИС ТП', 'http://fgis.economy.gov.ru/fgis/')
        ),
        (
            ('Транслитератор названий', STREET_TRANSLITERATOR),
            ('Подбор слов', 'https://wordstat.yandex.ru')
        ),
        (
            ('FAQ НЯК', 'https://tinyurl.com/FAQ-NYK'),
        )
)
