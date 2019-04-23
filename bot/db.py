from pony.orm import Database

from bot.config import db_creds

db = Database(provider='postgres', **db_creds)