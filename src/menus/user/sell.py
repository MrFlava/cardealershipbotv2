import enum
from src.menus.user.order import SellOrders
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from src.models import Sedan, Coupe, Suv, Sportcar, Cabrio, Wagon, DBSession
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import RegexHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class SellCars(BaseMenu):
    menu_name = "sell_cars"
    class States(enum.Enum):
        ACTION = 1
        SELL_ORDER = 2

    def sell_cars_menu(self, bot, update):
        sell_keyboard = [[InlineKeyboardButton('Седан', callback_data='sell_sedan'),
                          InlineKeyboardButton('Купе', callback_data='sell_coupe')],
                         [InlineKeyboardButton('Внедорожник', callback_data='sell_suv'),
                          InlineKeyboardButton('Спорткар', callback_data='sell_sportcar')],
                         [InlineKeyboardButton('Кабриолет', callback_data='sell_cabrio'),
                          InlineKeyboardButton('Универсал', callback_data='sell_wagon')]]
        reply_keyboard = InlineKeyboardMarkup(sell_keyboard)
        update.message.reply_text('Какой тип автомобиля Вы хотите купить?', reply_markup=reply_keyboard)
        return self.States.ACTION

    def keyboard_handlers(self, bot, update, user_data):
        query = update.callback_query
        user_data['button'] = query.data
        if user_data['button'] == 'sell_sedan':
            sedans = DBSession.query(Sedan)
            bot.send_message(text='Список доступных моделей:', chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
            for car in sedans:
                car_name = car.car_model
                description = car.description
                price = str(car.price)

                bot.send_message(
                    text='Название:{}'.format(car_name) + ' Описание:{}'.format(description) + ' Цена (в $):{}'.format(
                        price), chat_id=query.message.chat_id,
                    message_id=query.message.message_id)

        elif user_data['button'] == 'sell_coupe':
            coupe_cars = DBSession.query(Coupe)
            bot.send_message(text='Список доступных моделей:', chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
            for car in coupe_cars:
                car_name = car.car_model
                description = car.description
                price = str(car.price)

                bot.send_message(
                    text='Название:{}'.format(car_name) + ' Описание:{}'.format(description) + ' Цена (в $):{}'.format(
                        price), chat_id=query.message.chat_id,
                    message_id=query.message.message_id)

        elif user_data['button'] == 'sell_suv':
            suv_cars = DBSession.query(Suv)
            bot.send_message(text='Список доступных моделей:', chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
            for car in suv_cars:
                car_name = car.car_model
                description = car.description
                price = str(car.price)

                bot.send_message(
                    text='Название:{}'.format(car_name) + ' Описание:{}'.format(description) + ' Цена (в $):{}'.format(
                        price), chat_id=query.message.chat_id,
                    message_id=query.message.message_id)

        elif user_data['button'] == 'sell_sportcar':
            sport_cars = DBSession.query(Sportcar)
            bot.send_message(text='Список доступных моделей:', chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
            for car in sport_cars:
                car_name = car.car_model
                description = car.description
                price = str(car.price)

                bot.send_message(
                    text='Название:{}'.format(car_name) + ' Описание:{}'.format(description) + ' Цена (в $):{}'.format(
                        price), chat_id=query.message.chat_id,
                    message_id=query.message.message_id)
        elif user_data['button'] == 'sell_cabrio':
            cabriolet_cars = DBSession.query(Cabrio)
            bot.send_message(text='Список доступных моделей:', chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
            for car in cabriolet_cars:
                car_name = car.car_model
                description = car.description
                price = str(car.price)
                bot.send_message(
                    text='Название:{}'.format(car_name) + ' Описание:{}'.format(description) + ' Цена (в $):{}'.format(
                        price), chat_id=query.message.chat_id,
                    message_id=query.message.message_id)
        elif user_data['button'] == 'sell_wagon':
            wagon_cars = DBSession.query(Wagon)
            bot.send_message(text='Список доступных моделей:', chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
            for car in wagon_cars:
                car_name = car.car_model
                description = car.description
                price = str(car.price)

                bot.send_message(
                    text='Название:{}'.format(car_name) + ' Описание:{}'.format(description) + ' Цена (в $):{}'.format(
                        price), chat_id=query.message.chat_id,
                    message_id=query.message.message_id)
        buttons = [[KeyboardButton('Создать заявку на покупку')]]
        buttons_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        bot.send_message(chat_id=query.message.chat_id,
                         text='Нажмите кнопку "Создать заявку на покупку" '
                              'если выбрали автомобиль', reply_markup=buttons_markup)
        return self.States.ACTION

    def get_handler(self):
        sell_orders = SellOrders(self, bot = self.bot)

        handler = ConversationHandler(
            entry_points=[RegexHandler('Купить машину', self.sell_cars_menu)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.keyboard_handlers, pass_user_data=True),
                                     sell_orders.handler],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler
