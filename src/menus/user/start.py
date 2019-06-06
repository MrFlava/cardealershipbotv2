import enum
from src.menus.user.order import SellOrders
from src.models import DBSession, User
from src.menus.user.rent import RentCars
from src.menus.user.sell import SellCars
from botmanlib.menus.basemenu import BaseMenu
from telegram import KeyboardButton, ReplyKeyboardMarkup
from botmanlib.menus.helpers import unknown_command, add_to_db
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, RegexHandler

class StartMenu(BaseMenu):
    menu_name = "start_menu"
    class States(enum.Enum):
        ACTION = 1

    def start_menu(self, bot, update, user_data):
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
        buttons = [[KeyboardButton('Купить машину'), KeyboardButton('Арендовать машину')]]
        buttons_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Здравствуйте, я  бот-автосалон.Благодаря мне'
                              ' Вы можете купить или арендовать машину прямо в телеграме!'
                              ' Чем могу быть полезен?', reply_markup=buttons_markup)
        return StartMenu.States.ACTION

    def get_handler(self):
         sell_cars = SellCars(self, bot=self.bot)
         rent_cars = RentCars(self, bot=self.bot)
         handler = ConversationHandler(
                entry_points=[CommandHandler('start', self.start_menu, pass_user_data=True)],
                states={
                    self.States.ACTION: [sell_cars.handler,
                                         rent_cars.handler],
                },
         fallbacks=[MessageHandler(Filters.all, unknown_command(-1), pass_user_data=True)], allow_reentry=True)

         return handler
