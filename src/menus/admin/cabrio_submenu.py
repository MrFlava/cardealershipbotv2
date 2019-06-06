import enum
from src.models import Cabrio, DBSession
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class CabrioData(BaseMenu):

    menu_name = 'cabrio_submenu'

    class States(enum.Enum):

        ACTION = 1

    def cabrio_submenu(self, bot, update):
        query = update.callback_query
        submenu_suv = [[InlineKeyboardButton('Показать БД-автомобилей', callback_data='show_cabrio'),
                        InlineKeyboardButton('Удалить автомобиль из БД', callback_data='delete_cabrio')],
                       [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_cabrio'),
                        InlineKeyboardButton('Добавить автомобиль', callback_data='add_cabrio')]]
        reply_markup = InlineKeyboardMarkup(submenu_suv)
        bot.send_message(text='Выберите операцию:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_cabrio(self, bot, update):
        cabrios =DBSession.query(Cabrio)
        query = update.callback_query
        bot.send_message(text='Список кабриолетов:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        for cabri_car in cabrios:
            id_car = str(cabri_car.id_car)
            car_model = cabri_car.car_model
            description = cabri_car.description
            price = str(cabri_car.price)
            bot.send_message(
                text='Id-машины:{}'.format(id_car) + ' Название модели:{}'.format(
                    car_model) + 'Описание:{}'.format(
                    description) + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION

    """
    def add_cabrio(self, bot, update, user_data):

    def change_desc(self, bot, update, user_data):

    def delete_cabrio(self, bot, update, user_data):
    """

    def get_handler(self):

        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.cabrio_submenu, pattern='adm_cabrio')],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_cabrio, pattern='show_cabrio')],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler