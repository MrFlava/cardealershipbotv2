import enum
from src.models import DBSession, Cars
from botmanlib.menus.basemenu import BaseMenu
from src.menus.admin.add_cars import AddSportcar
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class SportcarsData(BaseMenu):

    menu_name = 'sportcars_submenu'

    class States(enum.Enum):

        ACTION = 1

    def sportcar_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_suv = [[InlineKeyboardButton('Показать автомобили', callback_data='Sportcar'),
                        InlineKeyboardButton('Удалить автомобиль', callback_data='delete_sportcar')],
                       [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_sportcar'),
                        InlineKeyboardButton('Добавить автомобиль', callback_data='add_sportcar')]]
        reply_markup = InlineKeyboardMarkup(submenu_suv)
        self.send_or_edit(user_data, text='Выберите операцию:', chat_id=query.message.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_sportcar(self, bot, update, user_data):
        query = update.callback_query
        sportcars = DBSession.query(Cars).filter(Cars.car_type == query.data).all()
        self.send_or_edit(user_data, text='Список спорткаров:', chat_id=query.message.chat_id)
        for sportcar in sportcars:
            car_model = sportcar.car_model
            description = sportcar.description
            price = str(sportcar.price)
            bot.send_message(
                text=' Название модели:{}'.format(car_model) + 'Описание:{}'.format(description)
                     + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id, message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        add_sportcar = AddSportcar(self, bot=self.bot)
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.sportcar_submenu, pattern='adm_sportcar', pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_sportcar, pattern='Sportcar', pass_user_data=True),
                                     add_sportcar.handler],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

