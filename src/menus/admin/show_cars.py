import enum
from src.models import DBSession, Car
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command, to_state
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class ShowCars(BaseMenu):
    menu_name = 'show_cars'

    class States(enum.Enum):
        ACTION = 1

    def car_types(self, bot, update, user_data):
        user = user_data['user']
        query = update.callback_query
        submenu_keyboard = [[InlineKeyboardButton('Седан', callback_data='Sedan'),
                             InlineKeyboardButton('Купе', callback_data='Coupe')],
                            [InlineKeyboardButton('Внедорожник', callback_data='SUV'),
                             InlineKeyboardButton('Спорткар', callback_data='Sportcar')],
                            [InlineKeyboardButton('Кабриолет', callback_data='Cabriolet'),
                             InlineKeyboardButton('Универсал', callback_data='Wagon')]]
        reply_markup = InlineKeyboardMarkup(submenu_keyboard)
        self.send_or_edit(user_data, text='Выберите тип кузова:', chat_id=user.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_car(self, bot, update, user_data):
        user = user_data['user']
        query = update.callback_query
        cars = DBSession.query(Car).filter(Car.type == query.data).all()
        self.send_or_edit(user_data, text='Список всех машин:', chat_id=user.chat_id)
        for car in cars:
            car_name = car.model
            description = car.description
            price = car.price
            bot.send_message(text='Название:{}'.format(car_name) + ' Описание:{}'.format(description)
                                  + ' Цена (в $):{}'.format(price), chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.car_types, pattern='show_cars', pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_car, pass_user_data=True),
                                     MessageHandler(Filters.all, to_state(self.States.ACTION))]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler
