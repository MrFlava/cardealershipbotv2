import enum
import formencode
from src.models import DBSession, Cars
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command, add_to_db
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class AddSedan(BaseMenu):

    menu_name = 'add_sedan'

    class States(enum.Enum):

        ACTION = 1
        RECORD = 2

    def add_sedan(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Хорошо, тогда введите: название модели описание и цену')
        return self.States.RECORD

    def record_car(self, bot, update, user_data):
        text = update.message.text
        if 'name' not in user_data:
            name = formencode.validators.String()
            user_data['name'] = name.to_python(text)
        elif 'desc' not in user_data:
            desc = formencode.validators.String()
            user_data['desc'] = desc.to_python(text)
        elif 'price' not in user_data:
            price = formencode.validators.Number()
            user_data['price'] = price.to_python(text)
            record_car = Cars(car_type='Sedan', car_model=user_data['name'], description=user_data['desc'],
                              price=user_data['price'])
            if not add_to_db(record_car, session=DBSession):
                return self.conv_fallback(user_data)

            del user_data['name']
            del user_data['desc']
            del user_data['price']

        self.send_or_edit(user_data, text='Отлично.Данные записаны!', chat_id=update.message.chat_id)
        return self.States.RECORD

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.add_sedan, pattern='add_sedan', pass_user_data=True)],
            states={
                self.States.RECORD: [
                    MessageHandler(Filters.text, self.record_car, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler


class AddCoupe(BaseMenu):

    menu_name = 'add_coupe'

    class States(enum.Enum):

        ACTION = 1
        RECORD = 2

    def add_coupe(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Хорошо, тогда введите: название модели описание и цену')
        return self.States.RECORD

    def record_car(self, bot, update, user_data):
        text = update.message.text
        if 'name' not in user_data:
            name = formencode.validators.String()
            user_data['name'] = name.to_python(text)
        elif 'desc' not in user_data:
            desc = formencode.validators.String()
            user_data['desc'] = desc.to_python(text)
        elif 'price' not in user_data:
            price = formencode.validators.Number()
            user_data['price'] = price.to_python(text)
            record_car = Cars(car_type='Coupe', car_model=user_data['name'], description=user_data['desc'],
                              price=user_data['price'])
            if not add_to_db(record_car, session=DBSession):
                return self.conv_fallback(user_data)

            del user_data['name']
            del user_data['desc']
            del user_data['price']

        self.send_or_edit(user_data, text='Отлично.Данные записаны!', chat_id=update.message.chat_id)
        return self.States.RECORD

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.add_coupe, pattern='add_coupe', pass_user_data=True)],
            states={
                self.States.RECORD:
                    [MessageHandler(Filters.text, self.record_car, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler


class AddSportcar(BaseMenu):

    menu_name = 'add_sportcar'

    class States(enum.Enum):

        ACTION = 1
        RECORD = 2

    def add_sportcar(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Хорошо, тогда введите: название модели описание и цену')
        return self.States.RECORD

    def record_car(self, bot, update, user_data):
        text = update.message.text
        if 'name' not in user_data:
            name = formencode.validators.String()
            user_data['name'] = name.to_python(text)
        elif 'desc' not in user_data:
            desc = formencode.validators.String()
            user_data['desc'] = desc.to_python(text)
        elif 'price' not in user_data:
            price = formencode.validators.Number()
            user_data['price'] = price.to_python(text)
            record_car = Cars(car_type='Sportcar', car_model=user_data['name'], description=user_data['desc'],
                              price=user_data['price'])
            if not add_to_db(record_car, session=DBSession):
                return self.conv_fallback(user_data)

            del user_data['name']
            del user_data['desc']
            del user_data['price']

        self.send_or_edit(user_data, text='Отлично.Данные записаны!', chat_id=update.message.chat_id)
        return self.States.RECORD

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.add_sportcar, pattern='add_sportcar', pass_user_data=True)],
            states={
                self.States.RECORD:
                    [MessageHandler(Filters.text, self.record_car, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler


class AddSUV(BaseMenu):

    menu_name = 'add_SUV'

    class States(enum.Enum):

        ACTION = 1
        RECORD = 2

    def add_SUV(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Хорошо, тогда введите: название модели описание и цену')
        return self.States.RECORD

    def record_car(self, bot, update, user_data):
        text = update.message.text
        if 'name' not in user_data:
            name = formencode.validators.String()
            user_data['name'] = name.to_python(text)
        elif 'desc' not in user_data:
            desc = formencode.validators.String()
            user_data['desc'] = desc.to_python(text)
        elif 'price' not in user_data:
            price = formencode.validators.Number()
            user_data['price'] = price.to_python(text)
            record_car = Cars(car_type='SUV', car_model=user_data['name'], description=user_data['desc'],
                              price=user_data['price'])
            if not add_to_db(record_car, session=DBSession):
                return self.conv_fallback(user_data)

            del user_data['name']
            del user_data['desc']
            del user_data['price']

        self.send_or_edit(user_data, text='Отлично.Данные записаны!', chat_id=update.message.chat_id)
        return self.States.RECORD

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.add_SUV, pattern='add_suv', pass_user_data=True)],
            states={
                self.States.RECORD:
                    [MessageHandler(Filters.text, self.record_car, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler


class AddCabrio(BaseMenu):

    menu_name = 'add_cabrio'

    class States(enum.Enum):

        ACTION = 1
        RECORD = 2

    def add_cabrio(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Хорошо, тогда введите: название модели описание и цену')
        return self.States.RECORD

    def record_car(self, bot, update, user_data):
        text = update.message.text
        if 'name' not in user_data:
            name = formencode.validators.String()
            user_data['name'] = name.to_python(text)
        elif 'desc' not in user_data:
            desc = formencode.validators.String()
            user_data['desc'] = desc.to_python(text)
        elif 'price' not in user_data:
            price = formencode.validators.Number()
            user_data['price'] = price.to_python(text)
            record_car = Cars(car_type='Cabriolet', car_model=user_data['name'], description=user_data['desc'],
                              price=user_data['price'])
            if not add_to_db(record_car, session=DBSession):
                return self.conv_fallback(user_data)

            del user_data['name']
            del user_data['desc']
            del user_data['price']

        self.send_or_edit(user_data, text='Отлично.Данные записаны!', chat_id=update.message.chat_id)
        return self.States.RECORD

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.add_cabrio, pattern='add_cabrio', pass_user_data=True)],
            states={
                self.States.RECORD:
                    [MessageHandler(Filters.text, self.record_car, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler

class AddWagon(BaseMenu):

    menu_name = 'add_wagon'

    class States(enum.Enum):

        ACTION = 1
        RECORD = 2

    def add_wagon(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Хорошо, тогда введите: название модели описание и цену')
        return self.States.RECORD

    def record_car(self, bot, update, user_data):
        text = update.message.text
        if 'name' not in user_data:
            name = formencode.validators.String()
            user_data['name'] = name.to_python(text)
        elif 'desc' not in user_data:
            desc = formencode.validators.String()
            user_data['desc'] = desc.to_python(text)
        elif 'price' not in user_data:
            price = formencode.validators.Number()
            user_data['price'] = price.to_python(text)
            record_car = Cars(car_type='Cabriolet', car_model=user_data['name'], description=user_data['desc'],
                              price=user_data['price'])
            if not add_to_db(record_car, session=DBSession):
                return self.conv_fallback(user_data)

            del user_data['name']
            del user_data['desc']
            del user_data['price']

        self.send_or_edit(user_data, text='Отлично.Данные записаны!', chat_id=update.message.chat_id)
        return self.States.RECORD

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.add_wagon, pattern='add_wagon', pass_user_data=True)],
            states={
                self.States.RECORD:
                    [MessageHandler(Filters.text, self.record_car, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

        return handler




