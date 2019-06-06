import enum
from src.models import Sedan, DBSession
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class SedansData(BaseMenu):
    menu_name = 'sedan_submenu'
    class States(enum.Enum):
        ACTION = 1

    def sedan_submenu(self, bot, update):
        query = update.callback_query
        submenu_seadns = [[InlineKeyboardButton('Показать БД-автомобилей', callback_data='show_sedans'),
                           InlineKeyboardButton('Удалить автомобиль из БД', callback_data='delete_sedan')],
                          [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_sedan'),
                           InlineKeyboardButton('Добавить автомобиль', callback_data='add_sedan')]]
        reply_markup = InlineKeyboardMarkup(submenu_seadns)
        bot.send_message(text='Выберите операцию:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_sedans(self, bot, update):
        sedans = DBSession.query(Sedan)
        query = update.callback_query
        bot.send_message(text='Список седанов:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        for sedan in sedans:
            id_car = str(sedan.id_car)
            car_model = sedan.car_model
            description = sedan.description
            price = str(sedan.price)
            bot.send_message(
                text='Id-машины:{}'.format(id_car) + ' Название модели:{}'.format(
                    car_model) + 'Описание:{}'.format(
                    description) + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION
    """
    def add_sedan(self, bot, update, user_data):
    
    def change_desc(self, bot, update, user_data):
    
    def delete_sedan(self, bot, update, user_data):
    """
    def get_handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.sedan_submenu, pattern='adm_sedan')],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_sedans, pattern='show_sedans')],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

