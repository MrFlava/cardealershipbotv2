import enum
from src.models import DBSession, Customer
from botmanlib.menus.helpers import to_state
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class ShowCustomers(BaseMenu):
    menu_name = 'show_customers_menu'

    class States(enum.Enum):
        ACTION = 1

    def customer_type(self, bot, update, user_data):
        user = user_data['user']
        buttons = [[InlineKeyboardButton('Покупатели', callback_data='Buyer'),
                    InlineKeyboardButton('Арендаторы', callback_data='Renter')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        self.send_or_edit(user_data, chat_id=user.chat_id,
                          text='Какой тип клиентов Вас интересует?', reply_markup=reply_markup)
        return self.States.ACTION

    def show_customer(self, bot, update, user_data):
        user = user_data['user']
        query = update.callback_query
        data = query.data
        customers = DBSession.query(Customer).filter(Customer.type == data).all()
        self.send_or_edit(user_data, text='Список клиентов:', chat_id=user.chat_id)
        for customer in customers:
            ordered_car = customer.ordered_car
            phone = customer.phone
            creating_data = customer.creating_date
            bot.send_message(text='Заказанная машина:{}'.format(ordered_car) + ' Телефон:{}'.format(phone)
                                  + ' Дата создания заказа:{}'.format(creating_data), chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.customer_type, pattern='show_customers', pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.show_customer, pass_user_data=True),
                                     MessageHandler(Filters.all, to_state(self.States.ACTION))]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler
