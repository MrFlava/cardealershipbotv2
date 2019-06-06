import enum
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from src.models import Rent_customer, Sell_customer, DBSession
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class CustomersData(BaseMenu):
    class States(enum.Enum):
        ACTION = 1

    def show_customers_menu(self, bot, update):
        query = update.callback_query
        submenu_keyboard = [[InlineKeyboardButton('Покупатели', callback_data='buyers'),
                             InlineKeyboardButton('Арндаторы', callback_data='rent_customers')]]
        reply_markup = InlineKeyboardMarkup(submenu_keyboard)
        bot.send_message(text='Выберите тип клиентов', chat_id=query.message.chat_id,
                         message_id=query.message.message_id, reply_markup=reply_markup)
        return self.States.ACTION

    def rent_customers_button(self, bot, update):
        customers = DBSession.query(Rent_customer)
        query = update.callback_query
        bot.send_message(text='Данные о арендаторах: ', chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        for customer in customers:
            id = str(customer.id_customer)
            phone = str(customer.phone)
            ordered_car = customer.ordered_car
            user_id = str(customer.user_id)
            creating_date = str(customer.creating_date)
            bot.send_message(
                text='Id-клиента:{}'.format(id) + ' Чат-id:{}'.format(user_id) + ' Заказанная машина:{}'.format(
                    ordered_car) + 'Телефон:{}'.format(phone) + 'Дата создания заказа:{}'.format(creating_date),
                chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION


    def buyers_button(self, bot, update):
        customers = DBSession.query(Sell_customer)
        query = update.callback_query
        bot.send_message(text='Данные о покупателях:', chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        for customer in customers:
            id = str(customer.id_customer)
            phone = str(customer.phone)
            ordered_car = customer.ordered_car
            user_id = str(customer.user_id)
            creating_date = str(customer.creating_date)
            bot.send_message(
                text='Id-клиента:{}'.format(id) + ' Чат-id:{}'.format(user_id) + ' Заказанная машина:{}'.format(
                    ordered_car) + 'Телефон:{}'.format(phone) + 'Дата создания заказа:{}'.format(creating_date),
                chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.show_customers_menu, pattern='show_customers')],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.buyers_button, pattern='buyers'),
                                     CallbackQueryHandler(self.rent_customers_button, pattern='rent_customer')],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

