import os
import logging
from telegram.ext import Updater
from botmanlib.bot import BotmanBot
from src.menus.user.start import StartMenu
from src.menus.admin.admin import AdminMenu
from src.settings import MEDIA_FOLDER, RESOURCES_FOLDER

logger = logging.getLogger(__name__)

def main():

    bot_token = os.environ['bot.token']
    bot = BotmanBot(token=bot_token)
    updater = Updater(bot=bot)
    dp = updater.dispatcher
    start_menu = StartMenu(bot=bot, dispatcher=dp)
    admin_menu = AdminMenu(bot=bot, dispatcher=dp)
    dp.add_handler(admin_menu.handler)
    dp.add_handler(start_menu.handler)


    if not os.path.exists(MEDIA_FOLDER):
        os.mkdir(MEDIA_FOLDER)
        logger.info("Media folder created")
    if not os.path.exists(RESOURCES_FOLDER):
        os.mkdir(RESOURCES_FOLDER)
        logger.info("Resources folder created")


    logger.info("Bot started")
    updater.start_polling()
    updater.idle()
    bot.stop()

if __name__ == "__main__":
    main()
