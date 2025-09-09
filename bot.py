import logging
from telegram.ext import Updater

import config
from handlers import (
    admin_handler,
    mode_handler,
    game_handler,
    txt_category_handler,
    affix_manage_handler,
    nh_handler,
    stats_handler,
    leaderboard_handler,
    settings_handler,
    start_handler,           # new start handler
    help_handler,            # new help handler
    exist_handler,
    info_handler,
    role_handler,
    rules_handler,
)
from utils.group_control import is_permitted
from utils.access_control import is_banned

def main():
    logging.basicConfig(level=logging.INFO)
    updater = Updater(config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # /start welcome
    start_handler.register(dp)

    # admin / sudo / broadcast  / group permissions
    admin_handler.register(dp)

    # mode starters: /animal, /prefix, etc.
    mode_handler.register(dp)

    # in-game logic: join, submission, timeouts
    game_handler.register(dp)

    # dictionary management
    txt_category_handler.register(dp)
    affix_manage_handler.register(dp)
    nh_handler.register(dp)

    # ← Add these three lines here:
    info_handler.register(dp)
    role_handler.register(dp)
    exist_handler.register(dp)
    rules_handler.register(dp)
    # ← end of utility handlers

    # help, social and settings
    help_handler.register(dp)
    stats_handler.register(dp)
    leaderboard_handler.register(dp)
    settings_handler.register(dp)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
