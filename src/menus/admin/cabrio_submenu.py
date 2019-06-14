import enum
from src.models import DBSession, Cars
from botmanlib.menus.basemenu import BaseMenu
from src.menus.admin.add_cars import AddCabrio
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class CabrioData(BaseMenu):

    menu_name = 'cabrio_submenu'

    class States(enum.Enum):

        ACTION = 1

    def cabrio_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_suv = [[InlineKeyboardButton('Показать автомобили', callback_data='Cabriolet'),
                        InlineKeyboardButton('Удалить автомобиль', callback_data='delete_cabrio')],
                       [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_cabrio'),
                        InlineKeyboardButton('Добавить автомобиль', callback_data='add_cabrio')]]
        reply_markup = InlineKeyboardMarkup(submenu_suv)
        self.send_or_edit(user_data, text='Выберите операцию:', chat_id=query.message.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_cabrio(self, bot, update, user_data):
        query = update.callback_query
        cabrios = DBSession.query(Cars).filter(Cars.car_type == query.data).all()
        self.send_or_edit(user_data, text='Список кабриолетов:', chat_id=query.message.chat_id)
        for cabri_car in cabrios:
            car_model = cabri_car.car_model
            description = cabri_car.description
            price = str(cabri_car.price)
            bot.send_message(
                text=' Название модели:{}'.format(car_model)
                + 'Описание:{}'.format(description) + ' Цена (в$):{}'.format(price),
                chat_id=query.message.chat_id, message_id=query.message.message_id)
        return self.States.ACTION


    def get_handler(self):
        add_cabrio = AddCabrio(self, bot=self.bot)
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.cabrio_submenu, pattern='adm_cabrio', pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_cabrio, pattern='Cabriolet', pass_user_data=True),
                                     add_cabrio.handler],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler
