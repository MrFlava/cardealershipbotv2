import enum
from src.models import User, DBSession
from src.local_settings import admin_password
from botmanlib.menus.basemenu import BaseMenu
from src.menus.admin.suv_submenu import SuvData
from botmanlib.menus.helpers import unknown_command
from src.menus.admin.wagon_submenu import WagonsData
from src.menus.admin.coupe_submenu import CoupesData
from src.menus.admin.sedan_submenu import SedansData
from src.menus.admin.cabrio_submenu import CabrioData
from src.menus.admin.customers_data import CustomersData
from src.menus.admin.sportcar_submenu import SportcarsData
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class AdminMenu(BaseMenu):
    menu_name = 'admin_menu'
    class States(enum.Enum):

        ACTION = 1


    def admin_menu(self, bot, update, user_data):

        text = update.message.text.replace('/admin', '')
        text = "".join(text.split())
        user_data['password'] = text
        if user_data['password'] == admin_password:
            admin_keyboard = [[InlineKeyboardButton('О правах администратора', callback_data='about'),
                               InlineKeyboardButton('Посмотреть БД-клиентов', callback_data='show_customers')],
                              [InlineKeyboardButton('Посмотреть БД-пользователей боота', callback_data='show_users'),
                               InlineKeyboardButton('Работа с БД-машин', callback_data='work_with_car_data')]]
            reply_markup = InlineKeyboardMarkup(admin_keyboard)
            update.message.reply_text('Активирован режим администратора!',
                                      reply_markup=reply_markup)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Ошибка! Пароль введен неверно, попробуйте снова.')
        return self.States.ACTION

    def about_button(self, bot, update):
        query = update.callback_query
        bot.send_message(text='Режим администратоатора позволяет просматривать данные пользователей, '
                              'клиентов и работать с БД-машин', chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        return self.States.ACTION

    def show_users_button(self, bot, update):
        users = DBSession.query(User)
        query = update.callback_query
        bot.send_message(text='Список всех пользователей бота:',
                         chat_id=query.message.chat_id, message_id=query.message.message_id)
        for user in users:
            id = str(user.id_user)
            chat_id = str(user.chat_id)
            name = user.nameACTION = 1
            username = user.username
            active = user.active
            join_date = str(user.join_date)
            bot.send_message(
                text='Id-пользователя:{}'.format(id) + ' Чат-id:{}'.format(chat_id) + ' Имя:{}'.format(
                    name) + 'Юзернейм:{}'.format(username) + 'Активность:{}'.format(active)
                     + 'Дата начала работы с ботом:{}'.format(join_date), chat_id=query.message.chat_id,
                message_id=query.message.message_id)
        return self.States.ACTION

    def cars_data_button(self, bot, update):
        query = update.callback_query
        submenu_keyboard = [[InlineKeyboardButton('Седан', callback_data='adm_sedan'),
                             InlineKeyboardButton('Купе', callback_data='adm_coupe')],
                            [InlineKeyboardButton('Внедорожник', callback_data='adm_suv'),
                             InlineKeyboardButton('Спорткар', callback_data='adm_sportcar')],
                            [InlineKeyboardButton('Кабриолет', callback_data='adm_cabrio'),
                             InlineKeyboardButton('Универсал', callback_data='adm_wagon')]]
        reply_markup = InlineKeyboardMarkup(submenu_keyboard)
        bot.send_message(text='Для начала выберите тип кузова машины', chat_id=query.message.chat_id,
                         message_id=query.message.message_id, reply_markup=reply_markup)
        return self.States.ACTION


    def get_handler(self):
        wagons_data = WagonsData(self, bot=self.bot)
        sportcars_data = SportcarsData(self, bot=self.bot)
        suv_data = SuvData(self, bot=self.bot)
        cabrio_data = CabrioData(self, bot=self.bot)
        coupes_data = CoupesData(self, bot=self.bot)
        sedans_data = SedansData(self, bot=self.bot)
        customers_data = CustomersData(self, bot=self.bot)
        handler = ConversationHandler(
                entry_points=[CommandHandler('admin', self.admin_menu, pass_user_data=True)],
                states={
                    self.States.ACTION: [CallbackQueryHandler(self.about_button, pattern='about'),
                                         CallbackQueryHandler(self.show_users_button, pattern='show_users'),
                                         CallbackQueryHandler(self.cars_data_button, pattern='work_with_car_data'),
                                         sedans_data.handler,  customers_data.handler,
                                         coupes_data.handler, cabrio_data.handler,
                                         suv_data.handler, sportcars_data .handler,
                                         wagons_data.handler],
                },
    fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler