import enum
from src.models import DBSession, Cars
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class WagonsData(BaseMenu):

    menu_name = 'wagon_submenu'

    class States(enum.Enum):
        ACTION = 1

    def wagon_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_suv = [[InlineKeyboardButton('Показать автомобил', callback_data='Wagon'),
                        InlineKeyboardButton('Удалить автомобиль', callback_data='delete_wagon')],
                       [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_wagon'),
                        InlineKeyboardButton('Добавить автомобиль', callback_data='add_wagon')]]
        reply_markup = InlineKeyboardMarkup(submenu_suv)
        self.send_or_edit(user_data, text='Выберите операцию:', chat_id=query.message.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_wagon(self, bot, update, user_data):
        query = update.callback_query
        wagons = DBSession.query(Cars).filter(Cars.car_type == query.data).all()
        self.send_or_edit(user_data, text='Список универсалов:', chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
        for wagon_car in wagons:
            car_model = wagon_car.car_model
            description = wagon_car.description
            price = str(wagon_car.price)
            bot.send_message(
                text=' Название модели:{}'.format(car_model)
                     + 'Описание:{}'.format(description) + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id)
        return self.States.ACTION


    def get_handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.wagon_submenu, pattern='adm_wagon', pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_wagon, pattern='Wagon', pass_user_data=True)],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

