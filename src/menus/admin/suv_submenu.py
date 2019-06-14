import enum
from src.models import DBSession, Cars
from src.menus.admin.add_cars import AddSUV
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class SuvData(BaseMenu):

    menu_name = 'suv_submenu'

    class States(enum.Enum):

        ACTION = 1

    def suv_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_suv = [[InlineKeyboardButton('Показать автомобили', callback_data='SUV'),
                        InlineKeyboardButton('Удалить автомобиль', callback_data='delete_suv')],
                       [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_suv'),
                        InlineKeyboardButton('Добавить автомобиль', callback_data='add_suv')]]
        reply_markup = InlineKeyboardMarkup(submenu_suv)
        self.send_or_edit(user_data, text='Выберите операцию:', chat_id=query.message.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_suv(self, bot, update, user_data):
        query = update.callback_query
        suv = DBSession.query(Cars).filter(Cars.car_type == query.data).all()
        self.send_or_edit(user_data, text='Список внедорожников:', chat_id=query.message.chat_id)
        for suv_car in suv:
            car_model = suv_car.car_model
            description = suv_car.description
            price = str(suv_car.price)
            bot.send_message(' Название модели:{}'.format(car_model)
                             + 'Описание:{}'.format(description) + ' Цена (в$):{}'.format(price),
                             chat_id=query.message.chat_id, message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        add_suv = AddSUV(self, bot=self.bot)
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.suv_submenu, pattern='adm_suv', pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_suv, pattern='SUV', pass_user_data=True),
                                     add_suv.handler],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

