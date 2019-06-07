import enum
from src.models import Suv, DBSession
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class SuvData(BaseMenu):

    menu_name = 'suv_submenu'

    class States(enum.Enum):

        ACTION = 1

    def suv_submenu(self,bot, update):
        query = update.callback_query
        submenu_suv = [[InlineKeyboardButton('Показать БД-автомобилей', callback_data='show_suv'),
                        InlineKeyboardButton('Удалить автомобиль из БД', callback_data='delete_suv')],
                       [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_suv'),
                        InlineKeyboardButton('Добавить автомобиль', callback_data='add_suv')]]
        reply_markup = InlineKeyboardMarkup(submenu_suv)
        bot.send_message(text='Выберите операцию:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_suv(self, bot, update):
        suv = DBSession.query(Suv)
        query = update.callback_query
        bot.send_message(text='Список внедорожников:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        for suv_car in suv:
            id_car = str(suv_car.id_car)
            car_model = suv_car.car_model
            description = suv_car.description
            price = str(suv_car.price)
            bot.send_message(
                text='Id-машины:{}'.format(id_car) + ' Название модели:{}'.format(
                    car_model) + 'Описание:{}'.format(
                    description) + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.suv_submenu, pattern='adm_suv')],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_suv, pattern='show_suv')],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

