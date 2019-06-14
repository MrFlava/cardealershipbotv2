import enum
from src.models import DBSession, Cars
from src.menus.admin.add_cars import AddCoupe
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class CoupesData(BaseMenu):

    menu_name = 'coupe_submenu'

    class States(enum.Enum):
         ACTION = 1

    def coupe_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_coupes = [[InlineKeyboardButton('Показать автомобили', callback_data='Coupe'),
                           InlineKeyboardButton('Удалить автомобиль', callback_data='delete_coupe')],
                          [InlineKeyboardButton('Изменить описание автомобиля', callback_data='desc_coupe'),
                           InlineKeyboardButton('Добавить автомобиль', callback_data='add_coupe')]]
        reply_markup = InlineKeyboardMarkup(submenu_coupes)
        self.send_or_edit(user_data, text='Выберите операцию:', chat_id=query.message.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_coupes(self, bot, update, user_data):
        query = update.callback_query
        coupes = DBSession.query(Cars).filter(Cars.car_type == query.data).all()
        self.send_or_edit(user_data, text='Список купе:', chat_id=query.message.chat_id)
        for coupe in coupes:
            car_model = coupe.car_model
            description = coupe.description
            price = str(coupe.price)
            bot.send_message(
                text='Название модели:{}'.format(car_model) + 'Описание:{}'.format(description)
                     + ' Цена (в$):{}'.format(price), chat_id=query.message.chat_id, message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
            add_coupe = AddCoupe(self, bot=self.bot)
            handler = ConversationHandler(
                entry_points=[CallbackQueryHandler(self.coupe_submenu, pattern='adm_coupe', pass_user_data=True)],
                states={
                    self.States.ACTION: [CallbackQueryHandler(self.show_coupes, pattern='Coupe ', pass_user_data=True),
                                         add_coupe.handler],
                },
                fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
            return handler
