import enum
from src.models import User, DBSession
from botmanlib.menus.basemenu import BaseMenu
from src.local_settings import admin_password
from src.menus.admin.cars_control import CarsListMenu
from src.menus.admin.show_customers import ShowCustomers
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from botmanlib.menus.helpers import unknown_command, add_to_db, to_state
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class AdminMenu(BaseMenu):

    menu_name = 'admin_menu'

    class States(enum.Enum):
        ACTION = 1
        END = 2

    def admin_menu(self, bot, update, user_data):
        user = DBSession.query(User).filter(User.chat_id == update.effective_user.id).first()
        if not user:
            user = User()
        tuser = update.effective_user
        user.chat_id = tuser.id
        user.name = tuser.full_name
        user.username = tuser.username
        user.active = True
        if not add_to_db(user, session=DBSession):
            return self.conv_fallback(user_data)
        user_data['user'] = user
        text = update.message.text.replace('/admin', '')
        text = "".join(text.split())
        user_data['password'] = text
        if user_data['password'] == admin_password:
            admin_keyboard = [[InlineKeyboardButton('О правах администратора', callback_data='about'),
                               InlineKeyboardButton('Данные клиентов', callback_data='show_customers')],
                              [InlineKeyboardButton('Данные пользователей', callback_data='show_users'),
                               InlineKeyboardButton('Данные машин', callback_data='cars_data')]]
            reply_markup = InlineKeyboardMarkup(admin_keyboard)
            update.message.reply_text('Активирован режим администратора!',
                                      reply_markup=reply_markup)
            return self.States.ACTION
        else:
            self.send_or_edit(user_data, chat_id=user.chat_id,
                              text='Ошибка! Пароль введен неверно, попробуйте снова.')
            return self.States.END

    def about_adminmode(self, bot, update, user_data):
        user = user_data['user']
        query = update.callback_query
        self.send_or_edit(user_data, text='Режим администратоатора позволяет просматривать данные пользователей, '
                                          'клиентов и работать с данными машин', chat_id=user.chat_id)
        return self.States.ACTION

    def show_users(self, bot, update, user_data):
        user = user_data['user']
        users = DBSession.query(User).all()
        query = update.callback_query
        self.send_or_edit(user_data, text='Список всех пользователей бота:', chat_id=user.chat_id)
        for user in users:
            name = user.name
            username = user.username
            active = user.active
            join_date = str(user.join_date)
            bot.send_message(
                text=' Имя:{}'.format(name) + 'Юзернейм:{}'.format(username) + 'Активность:{}'.format(active)
                     + 'Дата начала работы с ботом:{}'.format(join_date),
                chat_id=query.message.chat_id, message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        cars_list_menu = CarsListMenu(self)
        show_customers = ShowCustomers(self, bot=self.bot)
        handler = ConversationHandler(
            entry_points=[CommandHandler('admin', self.admin_menu, pass_user_data=True)],
            states={
                self.States.ACTION: [CallbackQueryHandler(self.about_adminmode, pattern='about', pass_user_data=True),
                                     CallbackQueryHandler(self.show_users,
                                                          pattern='show_users', pass_user_data=True),
                                     show_customers.handler, cars_list_menu.handler,
                                     MessageHandler(Filters.all, to_state(self.States.ACTION))],
                self.States.END: [CallbackQueryHandler(self.admin_menu, pass_user_data=True),
                                  MessageHandler(Filters.all, to_state(self.States.END))]
            },
            fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler
