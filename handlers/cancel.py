from telegram.ext import RegexHandler

from bot.helpers import cancel
from bot.phrases import MENU_RETURN

cancel_handler = RegexHandler(MENU_RETURN, cancel, pass_user_data=True)
