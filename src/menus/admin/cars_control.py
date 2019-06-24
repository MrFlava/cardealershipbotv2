import enum
from formencode import validators
from src.models import DBSession, Car
from telegram import InlineKeyboardButton
from botmanlib.menus import OneListMenu,  ArrowAddEditMenu
from telegram.ext import CallbackQueryHandler, ConversationHandler


class CarsListMenu(OneListMenu):

    menu_name = 'add_car_menu'
    model = Car
    add_delete_button = True

    class States(enum.Enum):
        ACTION = 1

    def entry(self, bot, update, user_data):
        if update.callback_query:
            bot.answer_callback_query(update.callback_query.id)
        return super(CarsListMenu, self).entry(bot, update, user_data)

    def query_objects(self, user_data):
        return DBSession.query(Car).all()

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^cars_control", pass_user_data=True)]

    def center_buttons(self, user_data, obj=None):
        _ = user_data['_']
        buttons = [InlineKeyboardButton("Добавить", callback_data="add_car")]
        if obj is not None:
            buttons.append(InlineKeyboardButton("Изменить", callback_data=f"edit_car_{obj.id}"))
        return buttons

    def message_text(self, obj, user_data):
        _ = user_data['_']

        message_text = "________" + "Автомобили" + "________\n"

        if obj:
            message_text += "Тип автомобиля: " + "{}".format(obj.type) + '\n'
            message_text += "Название автомобиля: " + "{}".format(obj.model) + '\n'
            message_text += "Описание: " + "{}".format(obj.description) + '\n'
            message_text += "Цена: " + "{}".format(obj.price) + '\n'
        else:
            message_text += "Ничего нет в списке" + '\n'

        return message_text

    def back(self, bot, update, **kwargs):
        user_data = kwargs['user_data']
        self.parent.send_message(user_data)
        return ConversationHandler.END

    def additional_states(self):
        cars_add_edit_menu = CarsAddEditMenu(self)
        return {
            self.States.ACTION: [cars_add_edit_menu.handler]
                }


class CarsAddEditMenu(ArrowAddEditMenu):

    menu_name = 'cars_add_edit_menu'
    model = Car
    variants_edit_mode = True
    show_reset_field = True
    reset_to_default = True

    def entry(self, bot, update, user_data):
        if self.menu_name not in user_data:
            user_data[self.menu_name] = {}
        data = update.callback_query.data
        if data.startswith("edit_car_"):
            user_data[self.menu_name]['car_id'] = int(data.replace("edit_car_", ""))
        else:
            user_data[self.menu_name]['car_id'] = None

        self._entry(bot, update, user_data)
        _ = user_data['_']
        if DBSession.query(Car.id).exists() is None:
            bot.answer_callback_query(update.callback_query.id, text="Для начала введите данные")
            return self.back(bot, update, user_data=user_data)

        self.is_new(user_data)
        self.load(user_data)
        self.send_message(user_data)
        return self.States.ACTION

    def query_object(self, user_data):
        if user_data[self.menu_name]['car_id']:
            return DBSession.query(Car).filter(Car.id == user_data[self.menu_name]['car_id']).all()
        else:
            return None

    def fields(self, user_data):
        _ = user_data['_']
        return [
            self.Field("type*", "*Тип авто", validators.OneOf(['SUV', 'Sportcar', 'Sedan',
                                                               'Cabriolet', 'Coupe', 'Wagon'])),
            self.Field('model*', '*Название', validators.String()),
            self.Field('description*', '*Описание', validators.String()),
            self.Field('price*', '*Цена', validators.Number())]

    def entry_points(self):
        return [CallbackQueryHandler(self.entry, pattern="^add_car$", pass_user_data=True),
                CallbackQueryHandler(self.entry, pattern="^edit_car_\d+$", pass_user_data=True)]

    def back(self, bot, update, **kwargs):
        user_data = kwargs['user_data']
        self.delete_interface(user_data)
        self.parent._get_objects(user_data, force_update=True)
        self.parent.send_message(user_data)
        return ConversationHandler.END

    def fill_field(self, bot, update, user_data):
        self.delete_interface(user_data)
        super(CarsAddEditMenu, self).fill_field(bot, update, user_data)

    def save(self, bot, update, user_data):
        _ = user_data['_']
        if not self.check_fields(user_data):
            self.delete_interface(user_data)
            bot.answer_callback_query(update.callback_query.id,
                                      text="Пожалуйста, заполните требуемые ячейки", show_alert=True)
            self.send_message(user_data)
            return self.States.ACTION
        self.delete_interface(user_data, 'Интерфейс убран')
        self.update_object(user_data)

        return self.back(bot, update, user_data=user_data)
