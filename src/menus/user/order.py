import enum
from formencode import validators
from src.models import Customer, DBSession
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command, add_to_db, to_state
from telegram.ext import MessageHandler, ConversationHandler, Filters, CallbackQueryHandler


class MakeOrder(BaseMenu):

    class States(enum.Enum):
        ACTION = 1

    menu_name = 'make_order_menu'

    def entry(self, bot, update, user_data):
        data = update.callback_query.data
        user = user_data['user']

        if self.menu_name not in user_data:
            user_data[self.menu_name] = {}

        user_data[self.menu_name]['customer_type'] = data
        user_data[self.menu_name]['ordered_car'] = None
        user_data[self.menu_name]['phone'] = None
        self.send_or_edit(user_data, chat_id=user.chat_id, text='Хорошо, тогда введите '
                                                                'название автомобиля и номер телефона.'
                                                                ' Служба тех. поддержки свяжется с '
                                                                'Вами для уточнения всех деталей и'
                                                                'заключения договора!')
        return MakeOrder.States.ACTION

    def add_order(self, bot, update, user_data):
        user = user_data['user']
        text = update.message.text
        if user_data[self.menu_name]['ordered_car'] is None:
            val = validators.String()
            car = val.to_python(text)
            user_data[self.menu_name]['ordered_car'] = car
        elif user_data[self.menu_name]['phone'] is None:
            val = validators.Number()
            value = val.to_python(text)
            user_data[self.menu_name]['phone'] = value
            add_order = Customer(type=user_data[self.menu_name]['customer_type'],
                                 ordered_car=user_data[self.menu_name]['ordered_car'],
                                 phone=user_data[self.menu_name]['phone'])
            if not add_to_db(add_order, session=DBSession):
                return self.conv_fallback(user_data)

        self.send_or_edit(user_data, chat_id=user.chat_id, text='Отлично, заявка принята! '
                                                                'В ближайщее время тех. '
                                                                'поддержка свяжется с Вами!')
        return MakeOrder.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.entry, pattern='Buyer|Renter', pass_user_data=True)],
            states={
                MakeOrder.States.ACTION: [MessageHandler(Filters.text, self.add_order, pass_user_data=True),
                                          MessageHandler(Filters.all, to_state(MakeOrder.States.ACTION))]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler
