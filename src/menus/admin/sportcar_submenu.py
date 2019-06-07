import enum
from src.models import Sportcar, DBSession
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class SportcarsData(BaseMenu):

    menu_name = 'sportcars_submenu'

    class States(enum.Enum):

        ACTION = 1

    def sportcar_submenu(self, bot, update):
        query = update.callback_query
        submenu_suv = [[InlineKeyboardButton('Показать БД-автомобилей', callback_data='show_sportcar'),
                        InlineKeyboardButton('Удалить автомобиль из БД', callback_data='delete_sportcar')],
                       [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_sportcar'),
                        InlineKeyboardButton('Добавить автомобиль', callback_data='add_sportcar')]]
        reply_markup = InlineKeyboardMarkup(submenu_suv)
        bot.send_message(text='Выберите операцию:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_sportcar(self, bot, update):
        sportcars = DBSession.query(Sportcar)
        query = update.callback_query
        bot.send_message(text='Список спорткаров:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        for sportcar in sportcars:
            id_car = str(sportcar.id_car)
            car_model = sportcar.car_model
            description = sportcar.description
            price = str(sportcar.price)
            bot.send_message(
                text='Id-машины:{}'.format(id_car) + ' Название модели:{}'.format(
                    car_model) + 'Описание:{}'.format(
                    description) + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.sportcar_submenu, pattern='adm_sportcar')],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_sportcar, pattern='show_sportcar')],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

