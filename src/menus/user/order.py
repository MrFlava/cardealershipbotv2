import enum
import formencode
from src.models import Customers, DBSession
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command, add_to_db
from telegram.ext import MessageHandler, ConversationHandler, RegexHandler, Filters

class SellOrders(BaseMenu):
    menu_name = 'order'
    class States(enum.Enum):
        ACTION = 1
        RECORD = 2

    def sell_order(self, bot, update, user_data):
        self.send_or_edit(user_data, chat_id=update.message.chat_id,
                          text='Хорошо, тогда введите название автомобиля и номер телефона.'
                               ' Служба тех. поддержки свяжется с Вами для уточнения всех деталей и'
                               'заключения договора о покупке!')
        return self.States.RECORD

    def sell_order_record(self, bot, update, user_data):
        text = update.message.text
        if 'car' not in user_data:
            car = formencode.validators.String()
            user_data['car'] = car.to_python(text)
        elif 'phone' not in user_data:
            phone = formencode.validators.Number()
            user_data['phone'] = phone.to_python(text)
            sell_car = Customers(customer_type='Buyer', ordered_car=user_data['car'],  phone=user_data['phone'])
            if not add_to_db(sell_car, session=DBSession):
                return self.conv_fallback(user_data)
            del user_data['phone']
            del user_data['car']

        self.send_or_edit(user_data, chat_id=update.effective_user.id, text='Отлично, заявка принята! '
                                                                    'В ближайщее время тех. поддержка свяжется с Вами!')
        return self.States.RECORD

    def get_handler(self):

        handler = ConversationHandler(entry_points=[
            RegexHandler('Создать заявку на покупку', self.sell_order, pass_user_data=True)],
            states={
                self.States.RECORD: [
                    MessageHandler(Filters.text, self.sell_order_record, pass_user_data=True)]
            }, fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler


class RentOrders(BaseMenu):
    
    class States(enum.Enum):
        ACTION = 1
        RECORD = 2

    def rent_order(self, bot, update, user_data):
        self.send_or_edit(user_data, chat_id=update.message.chat_id,
                         text='Хорошо, тогда введите название автомобиля и номер телефона.'
                              ' Служба тех. поддержки свяжется с Вами для уточнения всех деталей и '
                              'заключения договора о аренде! ')
        return self.States.RECORD

    def rent_order_record(self, bot, update, user_data):
        text = update.message.text
        if 'car' not in user_data:
            car = formencode.validators.String()
            user_data['car'] = car.to_python(text)
        elif 'phone' not in user_data:
            phone = formencode.validators.Number()
            user_data['phone'] = phone.to_python(text)
            sell_car = Customers(customer_type='Rent customer', ordered_car=user_data['car'], phone=user_data['phone'])
            if not add_to_db(sell_car, session=DBSession):
                return self.conv_fallback(user_data)
            del user_data['phone']
            del user_data['car']
        self.send_or_edit(user_data, chat_id=update.effective_user.id, text='Отлично, заявка принята! '
                                                                    'В ближайщее время тех. поддержка '
                                                                    'свяжется с Вами!')
        return self.States.RECORD

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
    RegexHandler('Перейти к оформлению заявки на аренду', self.rent_order, pass_user_data=True)],
                                      states={
                                          self.States.RECORD: [
                                              MessageHandler(Filters.text, self.rent_order_record, pass_user_data=True)]
                                      },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler
