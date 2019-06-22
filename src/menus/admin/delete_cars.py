import enum
import formencode
from src.models import DBSession, Cars
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class DeleteCars(BaseMenu):

    menu_name = 'delete_cars'

    class States(enum.Enum):
        ACTION = 1

    def delete_cars_button(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Хорошо, тогда введите название модели')
        return self.States.ACTION

    def delete_cars(self, bot, update, user_data):
        text = update.message.text
        if 'name' not in user_data:
            name = formencode.validators.String()
            user_data['name'] = name.to_python(text)
            deleted_car = DBSession.query(Cars).filter(Cars.car_model == user_data['name']).delete()
            DBSession.commit()
            del user_data['name']
        self.send_or_edit(user_data, text='Данные успешно удалены!')
        return self.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.delete_cars_button, pattern='delete_cars', pass_user_data=True)],
            states={
                self.States.ACTION:
                    [MessageHandler(Filters.text, self.delete_cars, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

