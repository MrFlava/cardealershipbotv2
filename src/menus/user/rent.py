import enum
from src.models import DBSession, Car
from src.menus.user.order import MakeOrder
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command, to_state
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import RegexHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class RentCars(BaseMenu):
    menu_name = "rent_cars"

    class States(enum.Enum):
        ACTION = 1

    def rent_cars(self, bot, update, user_data):
        user = user_data['user']
        rent_keyboard = [[InlineKeyboardButton('Седан', callback_data='Sedan'),
                          InlineKeyboardButton('Купе', callback_data='Coupe')],
                         [InlineKeyboardButton('Внедорожник', callback_data='SUV'),
                          InlineKeyboardButton('Спорткар', callback_data='Sportcar')],
                         [InlineKeyboardButton('Кабриолет', callback_data='Cabriolet'),
                          InlineKeyboardButton('Универсал', callback_data='Wagon')]]
        reply_keyboard = InlineKeyboardMarkup(rent_keyboard)
        update.message.reply_text('Какой тип автомобиля Вы хотите арендовать?', reply_markup=reply_keyboard)
        return self.States.ACTION

    def show_cars(self, bot, update, user_data):
        user = user_data['user']
        query = update.callback_query
        cars = DBSession.query(Car).filter(Car.type == query.data).all()
        self.send_or_edit(user_data, text='Список доступных моделей:', chat_id=user.chat_id)
        for car in cars:
            car_name = car.model
            description = car.description
            price = car.price
            bot.send_message(text='Название:{}'.format(car_name) + ' Описание:{}'.format(description)
                                  + ' Цена (в $):{}'.format(price), chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
        order_keyboard = [[InlineKeyboardButton('Перейти к оформлению заказа', callback_data='Renter')]]
        order_markup = InlineKeyboardMarkup(order_keyboard)
        self.send_or_edit(user_data, chat_id=user.chat_id,
                          text='Нажмите на кнопку "Перейти к оформлению заказа" '
                               'если выбрали автомобиль для аренды', reply_markup=order_markup)
        return self.States.ACTION

    def get_handler(self):
        rent_order = MakeOrder(self)
        handler = ConversationHandler(
            entry_points=[RegexHandler('Арендовать машину', self.rent_cars, pass_user_data=True)],
            states={
                self.States.ACTION: [rent_order.handler,  CallbackQueryHandler(self.show_cars, pass_user_data=True),
                                     MessageHandler(Filters.all, to_state(RentCars.States.ACTION))]},
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler
