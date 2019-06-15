import enum
from src.models import User, DBSession, Cars
from src.local_settings import admin_password
from botmanlib.menus.basemenu import BaseMenu
from botmanlib.menus.helpers import unknown_command
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.menus.admin.add_cars import AddSedan, AddCoupe, AddSUV, AddSportcar, AddCabrio, AddWagon
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters


class AdminMenu(BaseMenu):
    menu_name = 'admin_menu'

    class States(enum.Enum):
        ACTION = 1
        END = 2

    def admin_menu(self, bot, update, user_data):

        text = update.message.text.replace('/admin', '')
        text = "".join(text.split())
        user_data['password'] = text
        if user_data['password'] == admin_password:
            admin_keyboard = [[InlineKeyboardButton('О правах администратора', callback_data='about'),
                               InlineKeyboardButton('Данные клиентов', callback_data='show_customers')],
                              [InlineKeyboardButton('Данные пользователей', callback_data='show_users'),
                               InlineKeyboardButton('Данные машин', callback_data='car_data')]]
            reply_markup = InlineKeyboardMarkup(admin_keyboard)
            update.message.reply_text('Активирован режим администратора!',
                                      reply_markup=reply_markup)
            return self.States.ACTION
        else:
            self.send_or_edit(user_data, chat_id=update.message.chat_id,
                              text='Ошибка! Пароль введен неверно, попробуйте снова.')
            return self.States.END

    def about_button(self, bot, update, user_data):
        query = update.callback_query
        self.send_or_edit(user_data, text='Режим администратоатора позволяет просматривать данные пользователей, ' 
                                          'клиентов и работать с БД-машин', chat_id=query.message.chat_id)
        return self.States.ACTION

    def show_users_button(self, bot, update, user_data):

        users = DBSession.query(User).all()
        query = update.callback_query
        self.send_or_edit(user_data, text='Список всех пользователей бота:', chat_id=query.message.chat_id)
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

    def cars_data_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_keyboard = [[InlineKeyboardButton('Показать автомобили', callback_data='show_cars'),
                         InlineKeyboardButton('Удалить автомобиль', callback_data='delete_cars')],
                       [InlineKeyboardButton('Изменить описание', callback_data='desc_cars'),
                        InlineKeyboardButton('Добавить автомобиль', callback_data='add_cars')]]
        reply_markup = InlineKeyboardMarkup(submenu_keyboard)
        self.send_or_edit(user_data, text='Выберите операцию:', chat_id=query.message.chat_id, reply_markup=reply_markup)
        return self.States.ACTION

    def show_cars_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_keyboard = [[InlineKeyboardButton('Седан', callback_data='Sedan'),
                             InlineKeyboardButton('Купе', callback_data='Coupe')],
                            [InlineKeyboardButton('Внедорожник', callback_data='SUV'),
                             InlineKeyboardButton('Спорткар', callback_data='Sportcar')],
                            [InlineKeyboardButton('Кабриолет', callback_data='Cabriolet'),
                             InlineKeyboardButton('Универсал', callback_data='Wagon')]]
        reply_markup = InlineKeyboardMarkup(submenu_keyboard)
        self.send_or_edit(user_data, text='Выберите тип кузова:', chat_id=query.message.chat_id,
                          reply_markup=reply_markup)
        return self.States.ACTION

    def show_car(self, bot, update, user_data):
        query = update.callback_query
        cars = DBSession.query(Cars).filter(Cars.car_type == query.data).all()
        self.send_or_edit(user_data, text='Список всех машин:',
                          chat_id=query.message.chat_id)
        for car in cars:
            car_name = car.car_model
            description = car.description
            price = str(car.price)
            bot.send_message(text='Название:{}'.format(car_name) + ' Описание:{}'.format(description)
                                  + ' Цена (в $):{}'.format(price), chat_id=query.message.chat_id,
                             message_id=query.message.message_id)
        return self.States.ACTION

    def add_car_submenu(self, bot, update, user_data):
        query = update.callback_query
        submenu_keyboard = [[InlineKeyboardButton('Седан', callback_data='add_sedan'),
                             InlineKeyboardButton('Купе', callback_data='add_coupe')],
                            [InlineKeyboardButton('Внедорожник', callback_data='add_suv'),
                             InlineKeyboardButton('Спорткар', callback_data='add_sportcar')],
                            [InlineKeyboardButton('Кабриолет', callback_data='add_cabriolet'),
                             InlineKeyboardButton('Универсал', callback_data='add_wagon')]]
        reply_markup = InlineKeyboardMarkup(submenu_keyboard)
        bot.send_message(text='Выберите тип кузова:', chat_id=query.message.chat_id,
                        reply_markup=reply_markup, message_id=query.message.message_id)
        return self.States.ACTION

    def get_handler(self):
        add_sedan = AddSedan(self, bot=self.bot)
        add_coupe = AddCoupe(self, bot=self.bot)
        add_suv = AddSUV(self, bot=self.bot)
        add_sportcar = AddSportcar(self, bot=self.bot)
        add_cabriolet = AddCabrio(self, bot=self.bot)
        add_wagon = AddWagon(self, bot=self.bot)
        change_desc = ChangeDesc(self, bot=self.bot)
        handler = ConversationHandler(
                entry_points=[CommandHandler('admin', self.admin_menu, pass_user_data=True)],
                states={
                    self.States.ACTION: [CallbackQueryHandler(self.about_button, pattern='about', pass_user_data=True),
                                         CallbackQueryHandler(self.show_users_button, pattern='show_users', pass_user_data=True),
                                         CallbackQueryHandler(self.cars_data_submenu, pattern='car_data', pass_user_data=True),
                                         CallbackQueryHandler(self.show_cars_submenu, pattern='show_cars', pass_user_data=True),
                                         CallbackQueryHandler(self.add_car_submenu, pattern='add_cars', pass_user_data=True),
                                         change_desc.handler, add_sedan.handler,
                                         add_coupe.handler,
                                         add_suv.handler, add_sportcar.handler,
                                         add_cabriolet.handler, add_wagon.handler,
                                         CallbackQueryHandler(self.show_car, pass_user_data=True)],
                    self.States.END: [CallbackQueryHandler(self.admin_menu, pass_user_data=True)]
                },
    fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)
        return handler
