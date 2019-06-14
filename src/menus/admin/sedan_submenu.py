import enum
from src.models import DBSession, Cars
from src.menus.admin.add_cars import AddSedan
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class SedansData(BaseMenu):

    menu_name = 'sedan_submenu'

    class States(enum.Enum):
        ACTION = 1

    def sedan_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_seadns = [[InlineKeyboardButton('Показать автомобили', callback_data='Sedan'),
                           InlineKeyboardButton('Удалить автомобиль', callback_data='delete_sedan')],
                          [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_sedan'),
                           InlineKeyboardButton('Добавить автомобиль', callback_data='add_sedan')]]
        reply_markup = InlineKeyboardMarkup(submenu_seadns)
        self.send_or_edit(user_data, text='Выберите операцию:', chat_id=query.message.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_sedans(self, bot, update, user_data):
        query = update.callback_query
        sedans = DBSession.query(Cars).filter(Cars.car_type == query.data).all()
        self.send_or_edit(user_data, text='Список седанов:', chat_id=query.message.chat_id)
        for sedan in sedans:
            car_model = sedan.car_model
            description = sedan.description
            price = str(sedan.price)
            bot.send_message(
                text='Название модели:{}'.format(
                    car_model) + 'Описание:{}'.format(
                    description) + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        add_sedan = AddSedan(self, bot=self.bot)
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.sedan_submenu, pattern='adm_sedan', pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_sedans, pattern='Sedan', pass_user_data=True),
                                     add_sedan.handler],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

