import enum
from src.models import DBSession, Cars
from src.menus.user.order import RentOrders
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import RegexHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class RentCars(BaseMenu):

    menu_name = "rent_cars"

    class States(enum.Enum):

        ACTION = 1

    def rent_cars_menu(self, bot, update):
        rent_keyboard = [[InlineKeyboardButton('Седан', callback_data='Sedan'),
                          InlineKeyboardButton('Купе', callback_data='Coupe')],
                         [InlineKeyboardButton('Внедорожник', callback_data='SUV'),
                          InlineKeyboardButton('Спорткар', callback_data='Sportcar')],
                         [InlineKeyboardButton('Кабриолет', callback_data='Cabriolet'),
                          InlineKeyboardButton('Универсал', callback_data='Wagon')]]
        reply_keyboard = InlineKeyboardMarkup(rent_keyboard)
        update.message.reply_text('Какой тип автомобиля Вы хотите арендовать?', reply_markup=reply_keyboard)
        return self.States.ACTION

    def keyboard_handlers(self, bot, update, user_data):

        query = update.callback_query
        cars = DBSession.query(Cars).filter(Cars.car_type == query.data).all()
        self.send_or_edit(user_data, text='Список доступных моделей:', chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        for car in cars:
            car_name = car.car_model
            description = car.description
            price = str(car.price)
            bot.send_message(text='Название:{}'.format(car_name) + ' Описание:{}'.format(description)
                 + ' Цена (в $):{}'.format(price), chat_id=query.message.chat_id, message_id=query.message.message_id)
        buttons = [[KeyboardButton('Перейти к оформлению заявки на аренду')]]
        buttons_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        bot.send_message(chat_id=query.message.chat_id,
                         text='Нажмите на кнопку "Перейти к оформлению заявки на аренду" '
                              'если выбрали автомобиль для аренды', reply_markup=buttons_markup)
        return self.States.ACTION

    def get_handler(self):
        rent_orders = RentOrders(self, bot=self.bot)
        handler = ConversationHandler(
            entry_points=[RegexHandler('Арендовать машину', self.rent_cars_menu)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.keyboard_handlers, pass_user_data=True),
                                     rent_orders.handler]},
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler
