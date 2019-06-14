import enum
from src.models import Customers, DBSession
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class CustomersData(BaseMenu):

    class States(enum.Enum):
        ACTION = 1

    def show_customers_menu(self, bot, update, user_data):
        query = update.callback_query
        submenu_keyboard = [[InlineKeyboardButton('Покупатели', callback_data='Buyer'),
                             InlineKeyboardButton('Арндаторы', callback_data='Rent_customer')]]
        reply_markup = InlineKeyboardMarkup(submenu_keyboard)
        self.send_or_edit(user_data, text='Выберите тип клиентов', chat_id=query.message.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_customers(self, bot, update, user_data):
        query = update.callback_query
        customers = DBSession.query(Customers).filter(Customers.customer_type == query.data).all()
        self.send_or_edit(user_data, text='Данные о клиентах: ', chat_id=query.message.chat_id,)
        for customer in customers:
            phone = str(customer.phone)
            ordered_car = customer.ordered_car
            creating_date = str(customer.creating_date)
            bot.send_message(
                text='Заказанная машина:{}'.format(ordered_car) + 'Телефон:{}'.format(phone) +
                     'Дата создания заказа:{}'.format(creating_date), chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(self.show_customers_menu, pattern='show_customers', pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_customers, pass_user_data=True)],
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

