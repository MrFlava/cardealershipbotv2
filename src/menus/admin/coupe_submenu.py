import enum
from src.models import Coupe, DBSession
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class CoupesData(BaseMenu):

    menu_name = 'coupe_submenu'

    class States(enum.Enum):

         ACTION = 1

    def coupe_submenu(self, bot, update):
        query = update.callback_query
        submenu_coupes = [[InlineKeyboardButton('Показать БД-автомобилей', callback_data='show_coupes'),
                           InlineKeyboardButton('Удалить автомобиль из БД', callback_data='delete_coupe')],
                          [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_coupe'),
                           InlineKeyboardButton('Добавить автомобиль', callback_data='add_coupe')]]
        reply_markup = InlineKeyboardMarkup(submenu_coupes)
        bot.send_message(text='Выберите операцию:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_coupes(self, bot, update):
        coupes = DBSession.query(Coupe)
        query = update.callback_query
        bot.send_message(text='Список купе:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        for coupe in coupes:
            id_car = str(coupe.id_car)
            car_model = coupe.car_model
            description = coupe.description
            price = str(coupe.price)
            bot.send_message(
                text='Id-машины:{}'.format(id_car) + ' Название модели:{}'.format(
                    car_model) + 'Описание:{}'.format(
                    description) + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
            handler = ConversationHandler(
                entry_points=[CallbackQueryHandler(self.coupe_submenu, pattern='adm_coupe')],
                states={
                    self.States.ACTION: [CallbackQueryHandler(self.show_coupes, pattern='show_coupes')],
                },
                fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
            return handler
