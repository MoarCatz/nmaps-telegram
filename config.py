import os
import re
from algoliasearch import algoliasearch
from phrases import *

telegram_key = os.getenv('TELEGRAM_API_KEY',
                         '331488080:AAH8PEA9WnsZtFubYnwFI5EWDq1fvqb9ZAE')

client = algoliasearch.Client(os.getenv('ALGOLIA_CLIENT', 'key'),
                              os.getenv('ALGOLIASEARCH_API_KEY_SEARCH', 'key'))

links = client.init_index('links')
rules = client.init_index('rules')
rubrics = client.init_index('rubrics')
indices = (links, rules, rubrics)

screen_hashtags = re.compile('.*#({}|{}).*'.format(HASH_SCREEN,
                                                   HASH_SCREEN_ENG),
                             flags=re.S | re.I)
road_hashtag = re.compile('.*#({}|{}|{}|{}).*'.format(HASH_ROADBLOCK,
                                                      HASH_ROADBLOCK_ENG,
                                                      HASH_ROAD,
                                                      HASH_ROAD_ENG),
                          flags=re.S | re.I)

FEEDBACK_REQUESTED, SEARCH_QUERY_REQUESTED, TRANSLITERATE_REQUESTED = 1, 1, 1

main_menu = [[MENU_LINKS],
             [MENU_TRANSLIT],
             [MENU_SEARCH_CLUB, MENU_SEARCH_RULES],
             [MENU_ROADS, MENU_FEEDBACK]]

admin_menu = [[MENU_CHATS],
              [MENU_RETURN]]

nmaps_chat = int(os.getenv('NMAPSCHAT', '-1001136617457'))
mods_chat = int(os.getenv('MODSCHAT', '-1001304260305'))
roads_chat = int(os.getenv('ROADSCHAT', '-259382209'))
english_chat = -1001308645324

alexfox = 30375360
bforest = 291582989
admins = list(map(int, os.getenv('ADMINS',
                                 '{},{}'.format(alexfox, bforest)).split(',')))
roads_staff = os.getenv('ROADS_STAFF', 'Bagirov').split(',')

instantview_url = 'https://t.me/iv?url={}&rhash=082e533d0deed1'
rules_search_url = 'https://yandex.ru/support/search-results/?service=nmaps&query='
club_search_url = 'https://yandex.ru/blog/narod-karta/search?text='
transliterator = 'https://script.google.com/macros/s/AKfycbwCfGxk22dNUACxjRMULtVo4UzzRwfk49g9rIy-yycPMACtEps2/exec?'
