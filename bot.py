#!/usr/bin/python
# -*- coding: utf-8 -*-

import emoji
import time
import config
import dbhelper
import logging
import telebot
from telebot import TeleBot, types
from config import token
from dbhelper import DBHelper, SessionDb
from buttons import crypto_sell_buttons, main_buttons_without_img, \
    currency_site_buttons, marginality_amount_buttons
from utils import create_inline_keyboard, create_keyboard, formatItems

bot = TeleBot(token)
logger = telebot.logger
telebot.logger.setLevel(logging.ERROR)

db = DBHelper()
session = SessionDb()
db.setup()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте, я mdCryptoBot. Ваш бот в сфере криптовалют")
    bot.send_message(
        message.chat.id, "Пожалуйста, выберите из списка одну из услуг...",
        reply_markup=create_keyboard(main_buttons_without_img, 1)
    )
    dbhelper.set_state(message.chat.id, config.States.S_CHOOSE_CRYPTO.value)


@bot.message_handler(commands=['Продать'])
def send_crypto(message):
    print('ПРОДАТЬ COMMAND WORKING')
    bot.send_message(
        message.chat.id, "Пожалуйста, выберите криптовалюту из списка",
        reply_markup=create_inline_keyboard(crypto_sell_buttons, type='crypto')
    )
    dbhelper.get_current_state(message.chat.id)


# По команде /Сбросить будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["Сбросить"])
def cmd_reset(message):
    bot.send_message(
        message.chat.id, "Все ваши действия были отменены. Пожалуйста, выберите из списка одну из услуг...",
        reply_markup=create_inline_keyboard(crypto_sell_buttons, type='crypto')
    )
    dbhelper.set_state(message.chat.id, config.States.S_CHOOSE_CRYPTO.value)


@bot.message_handler(commands=["Главная"])
def cmd_reset(message):
    bot.send_message(
        message.chat.id, "Пожалуйста, выберите из списка одну из услуг...",
        reply_markup=create_keyboard(main_buttons_without_img, 1)
    )
    dbhelper.set_state(message.chat.id, config.States.S_CHOOSE_CRYPTO.value)


@bot.message_handler(commands=["Мои_объявления"])
def get_own_orders(message):
    print('МОИ ОБЪЯВЛЕНИЯ')
    orders = db.get_own_orders(message.chat.id)
    for order in orders:
        text = "Вы продаете: {} \nСумма: {} \nЦена по курсу: {} \nГород: {} \nКомиссия в процентах: {}\n\n". \
            format(order[2], order[3], order[4], order[5], order[6])
        bot.send_message(message.chat.id, text, reply_markup=create_inline_keyboard(order, 'deleteOrder'))


@bot.message_handler(commands=["Купить"])
def get_own_orders(message):
    print('КУПИТЬ')
    chat_id = message.chat.id
    orders = db.get_orders()
    for order in orders:
        user = bot.get_chat(order[1])
        username = str()
        if hasattr(user, 'username'):
            username = "@{}".format(user.username)
        else:
            username = "{} {}".format(user.first_name, user.last_name)
        print('username is {}'.format(username))

        text = "{} продает: {} \nСумма: {} \nЦена по курсу: {} \nГород: {} \nКомиссия в процентах: {}\n\n". \
            format(username, order[2], order[3], order[4], order[5], order[6])
        bot.send_message(chat_id, text)


    #####################################################################################################################
    """
     Handlers
    """


# # 2 - ENTER_SUM
# @bot.message_handler(func=lambda message: dbhelper.get_current_state(message.chat.id) == config.States.S_ENTER_SUM.value)
# def user_entering_crypto(message):
#     print('S_ENTER_SUM look')
#     chat_id = message.chat.id
#     print(message.text)
#     state = dbhelper.get_current_state(message.chat.id)
#     print('state is {}'.format(state))
#     bot.send_message(message.chat.id, "На какую сумму продаете($)?")
#     dbhelper.set_state(chat_id, config.States.S_CHOOSE_CURRENCY_SITE.value)


# 2 - ENTER OWN CRYPTO
@bot.message_handler(
    func=lambda message: dbhelper.get_current_state(message.chat.id) == config.States.S_TYPE_OWN_CRYPTO.value)
def user_own_currency(message):
    print('S_TYPE_OWN_CURRENCY_SITE is called')
    chat_id = message.chat.id
    crypto = message.text
    print(crypto)
    bot.send_message(
        chat_id, 'На какую сумму продаете($)?',
        reply_markup=create_keyboard(['/Сбросить', '/Главная'], 1)
    )
    session.create_session_with_crypto(chat_id, crypto=crypto)
    dbhelper.set_state(chat_id, config.States.S_CHOOSE_CURRENCY_SITE.value)
    print('--------------------------------------------------------------------')


# 4 - CHHOSE CURRENCY
@bot.message_handler(
    func=lambda message: dbhelper.get_current_state(message.chat.id) == config.States.S_CHOOSE_CURRENCY_SITE.value)
def user_entering_currency(message):
    print('S_ENTER_CURRENCY_SITE is called')
    chat_id = message.chat.id
    price = message.text
    print(price)
    bot.send_message(
        message.chat.id, "По какому курсу продаете?",
        reply_markup=create_inline_keyboard(currency_site_buttons, type='currency')
    )
    session.update_session(chat_id, price=price)
    print('--------------------------------------------------------------------')


# 5 - ENTER OWN CURRENCY SITE
@bot.message_handler(
    func=lambda message: dbhelper.get_current_state(message.chat.id) == config.States.S_TYPE_OWN_CURRENCY_SITE.value)
def user_entering_currency(message):
    print('S_TYPE_OWN_CURRENCY_SITE is called')
    chat_id = message.chat.id
    cur_site = message.text
    print(cur_site)
    bot.send_message(
        chat_id, 'В каком городе продаете?',
        reply_markup=create_keyboard(['/Сбросить', '/Главная'], 1)
    )
    session.update_session(chat_id, cur_site=cur_site)
    dbhelper.set_state(chat_id, config.States.S_ENTER_CITY.value)
    print('--------------------------------------------------------------------')



# 6 - ENTER CITY
@bot.message_handler(
    func=lambda message: dbhelper.get_current_state(message.chat.id) == config.States.S_ENTER_CITY.value)
def user_entering_city(message):
    print('S_ENTER_CITY is working')
    chat_id = message.chat.id
    city = message.text
    print(city)
    bot.send_message(
        chat_id, "Выберите размер комиссии (%)",
        reply_markup=create_inline_keyboard(marginality_amount_buttons, type='marginality')
    )
    session.update_session(chat_id, city=city)
    dbhelper.set_state(chat_id, config.States.S_CHOOSE_MARGINALITY.value)
    print('--------------------------------------------------------------------')


# # 5 - CHOOSE MARGINALITY
# @bot.message_handler(func=lambda message: dbhelper.get_current_state(message.chat.id) == config.States.S_CHOOSE_MARGINALITY.value)
# def user_entering_sum(message):
#     print('S_CHOOSE_MARGINALITY N is working')
#     city = message.text
#     print(city)
#     state = dbhelper.get_current_state(message.chat.id)
#     print('state is {}'.format(state))
#     bot.send_message(
#         message.chat.id, "Запись успешна добавлена",
#         reply_markup=create_keyboard(main_buttons_without_img, 1)
#     )
#     session.update_session(message.chat_id, city=city)
#     dbhelper.set_state(message.chat.id, config.States.S_START.value)


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    print('CALLBACK IS CALLED')
    print(call.data)
    chat_id = call.message.chat.id
    data = call.data.split('.')
    type = data[0]
    id = int(''.join(filter(lambda x: x.isdigit(), data[-1])))
    if type == 'crypto':
        if id != 26:
            bot.send_message(
                chat_id, 'На какую сумму продаете($)?',
                reply_markup=create_keyboard(['/Сбросить', '/Главная'], 1)
            )
            # Create session object
            crypto = ''.join(filter(lambda x: x.isalpha() or x in ['(', ')'], crypto_sell_buttons[id]))
            session.create_session_with_crypto(chat_id, crypto)
            dbhelper.set_state(chat_id, config.States.S_CHOOSE_CURRENCY_SITE.value)
        else:
            print('other')

            bot.send_message(
                chat_id, 'Пожалуйста, введите собственный вариант названия криптовалюты...',
                reply_markup=create_keyboard(['/Сбросить', '/Главная'], 1)
            )
            dbhelper.set_state(chat_id, config.States.S_TYPE_OWN_CRYPTO.value)

        print('--------------------------------------------------------------------')

    elif type == 'currency':
        if id != 8:
            cur_list = currency_site_buttons[id - 1].split('.')[1:]
            cur_site = '{}.{}'.format(cur_list[0], cur_list[1])
            print('cur_site is {}'.format(cur_site))
            bot.send_message(
                chat_id, 'В каком городе продаете?',
                reply_markup=create_keyboard(['/Сбросить', '/Главная'], 1)
            )
            session.update_session(chat_id, cur_site=cur_site)
            dbhelper.set_state(chat_id, config.States.S_ENTER_CITY.value)
        else:
            print('other currency')
            bot.send_message(
                chat_id, "Пожалуйста, введите собственный вариант сайта с курсом криптовалют..."
            )
            dbhelper.set_state(chat_id, config.States.S_TYPE_OWN_CURRENCY_SITE.value)
        print('--------------------------------------------------------------------')

    elif type == 'marginality':
        # if data[-1].contains
        marginality = marginality_amount_buttons[id].split()[-1]
        print(marginality)
        bot.send_message(
            call.message.chat.id, "Запись успешна добавлена",
            reply_markup=create_keyboard(main_buttons_without_img, 1)
        )
        session.update_session(chat_id, marginality=marginality)
        order = session.get_session(chat_id)
        print(order)
        crypto, price, cur_site, city, marginality = order['crypto'], order['price'], \
                                                     order['cur_site'], order['city'], order['marginality']

        db.add_order(chat_id, crypto, price, cur_site, city, marginality)
        dbhelper.set_state(call.message.chat.id, config.States.S_START.value)
        print('--------------------------------------------------------------------')

    elif type == 'deleteOrder':
        db.delete_order(id)
        db.get_own_orders(chat_id)
        print('deleted')
        bot.send_message(
            chat_id, 'Объявление успешно удалено',
            reply_markup=create_keyboard(main_buttons_without_img, 1)
        )
        print('--------------------------------------------------------------------')


print('Bot has been switched on')
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as ex:
            logger.error(ex)
            time.sleep(5)
