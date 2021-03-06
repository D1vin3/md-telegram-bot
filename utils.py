from telebot import types


def getItems(text):
    t = text.split(" ")
    return t[0], t[1], t[2], t[3]


def formatItems(isOwn, array):
    text = ""
    if not array:
        return 'К сожалению пока нет записей.'
    else:
        for elem in array:
            text += "{} продает: {} \nКоличество: {} \nЦена в долларах: {}\nКомиссия в процентах: {} \n\n".format(elem[1], elem[2], elem[3], elem[4], elem[5])
    return text


def create_keyboard(words=None, width=None):
        keyboard = types.ReplyKeyboardMarkup(row_width=width, resize_keyboard=True)
        for word in words:
            keyboard.add(types.KeyboardButton(text=word))
        return keyboard


def create_inline_keyboard(orders, type=None):
        keyboard = types.InlineKeyboardMarkup()
        callback_data = 'empty'

        if type == 'deleteOrder':
            return create_inline_button_for_delete(orders)
        for i in range(len(orders)):
            if type == 'marginality':
                callback_data = '{}.{}'.format(type, orders[i])
            elif type == 'crypto' or type == 'currency':
                item_id = str(int(orders[i].split('.')[0]))
                callback_data = '{}.{}'.format(type, item_id)
            btn = types.InlineKeyboardButton(text=orders[i], callback_data=callback_data)
            keyboard.add(btn)
        return keyboard


def create_inline_button_for_delete(order):
    keyboard = types.InlineKeyboardMarkup()
    callback_data = 'deleteOrder.{}'.format(order[0])
    btn = types.InlineKeyboardButton(text='Удалить объявление', callback_data=callback_data)
    keyboard.add(btn)
    return keyboard


def create_inline_keyboard_for_html(orders):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(orders)):
        btn = types.InlineKeyboardButton(text=orders[i], callback_data=orders[i])
        keyboard.add(btn)
    return keyboard
