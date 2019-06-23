import enum
from formencode import validators
from src.models import DBSession, Car
from botmanlib.menus.helpers import unknown_command
from botmanlib.menus import OneListMenu,  ArrowAddEditMenu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class CarsListMenu(OneListMenu):

    menu_name = 'add_car_menu'

    class States(enum.Enum):
        ACTION = 1

#class CrsAddEditMenu(ArrowAddEditMenu):