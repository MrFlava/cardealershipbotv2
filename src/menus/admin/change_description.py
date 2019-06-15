import enum
import formencode
from src.models import DBSession, Cars
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command, add_to_db
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

class ChangeDesc(BaseMenu):

    menu_name = 'change_desc'

    class States(enum.Enum):
        ACTION = 1

    def change_desc(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Хорошо, тогда введите название модели и новое описание')
        return self.States.ACTION

    def record_desc(self, bot, update, user_data):
        text = update.message.text
        if 'name' not in user_data:
            name = formencode.validators.String()
            user_data['name'] = name.to_python(text)
        elif 'new_desc' not in user_data:
            desc = formencode.validators.String()
            user_data['new_desc'] = desc.to_python(text)
            new_desc = DBSession.query(Cars).filter(Cars.car_model == user_data['name']).update({Cars.description: user_data['new_desc']}, synchronize_session=False)
            DBSession.commit()
            del user_data['name']
            del user_data['new_desc']
        self.send_or_edit(user_data, text='Изминения записаны в базу данных! ')
        return self.States.ACTION

    def get_handler(self):
        handler = ConversationHandler(entry_points=[
            CallbackQueryHandler(self.change_desc, pattern='desc_cars', pass_user_data=True)],
            states={
                self.States.ACTION:
                    [MessageHandler(Filters.text, self.record_desc, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler

