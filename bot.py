#!/usr/bin/python
# -*- coding: utf-8 -*-
import config
import telebot
import random
import json
from telebot import types

bot = telebot.TeleBot(config.token)

media = json.load(open("test.json", mode='r'))


def last_mamont(i):
    with open('test.json', 'r') as jfr:
        jf_file = json.load(jfr)

    with open('test.json', 'w') as outfile:
        jf_file['id'][i]['score'] += 1

        json.dump(jf_file, outfile, indent=4)


def equal(msg):
    for i in range(len(media['id'])):
        if media['id'][i]['global_id'] == msg:
            last_mamont(i)


def new_mamont(id, name, score):
    with open('test.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('test.json', 'w') as jf:
        jf_target = jf_file['id']
        user_info = {'global_id': id, 'name': name, 'score': score}
        jf_target.append(user_info)
        print(user_info)
        json.dump(jf_file, jf,indent=4)

def check_mamont(id):
    for some_id in range(len(media['id'])):
        if int(id) == int(media['id'][some_id]['global_id']):
            return True

@bot.message_handler(commands=["start", "home"])
def knb(message):
    # str(message.chat.last_name+' '+message.chat.first_name ) - проблемы с кодировкой
    if check_mamont(message.chat.id) != False:
        new_mamont(message.chat.id, str(message.chat.first_name), 1)

    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    kamen = types.KeyboardButton(text="камень")
    noj = types.KeyboardButton(text="ножницы")
    paper = types.KeyboardButton(text="бумага")
    donate = types.KeyboardButton(text="добавить попыток")
    record = types.KeyboardButton(text="рекорды")
    keyboard.add(kamen, noj, paper, donate, record)
    bot.send_message(message.chat.id, "камень? ножницы? бумага?",
                     reply_markup=keyboard)


@bot.message_handler(func=lambda msg: msg.text in config.spisok)
def kamens(msg):
    if config.tree == 0:
        bot.send_message(msg.chat.id, "количество попыток кончилось -  заплати \nQiwi - +79017698060")
        return
    bot_result = random.randint(0, 2)
    bot.send_message(msg.chat.id, "бот говорит: " + config.spisok[bot_result])
    d = bot_result - config.spisok.index(msg.text)

    if d > 0:
        if (d % 2) == 1:
            bot.send_message(msg.chat.id, "победа")
            equal(msg.chat.id)
            config.tree = 3
        else:
            bot.send_message(msg.chat.id, "поражение")
            config.tree -= 1
            bot.send_message(msg.chat.id, "количество оставшихся попыток: " + str(config.tree))

    elif d < 0:
        if (d % 2) == 0:
            bot.send_message(msg.chat.id, "победа")
            equal(msg.chat.id)
            config.tree = 3
        else:
            bot.send_message(msg.chat.id, "поражение")
            config.tree -= 1
            bot.send_message(msg.chat.id, "количество оставшихся попыток: " + str(config.tree))

        else:
            bot.send_message(msg.chat.id, "ничья")
            config.tree -= 1
            bot.send_message(msg.chat.id, "количество оставшихся попыток: " + str(config.tree))


@bot.message_handler(func=lambda msg: msg.text == "добавить попыток")
def don(msg):
    config.tree = 3
    bot.send_message(msg.chat.id, "количество оставшийся попыток: " + str(config.tree))


@bot.message_handler(func=lambda msg: msg.text == "рекорды")
def rec(msg):
    media = json.load(open("test.json", mode='r'))
    per = ''
    for k in media.get("id"):
        # print((str(k.get('global_id')) + '--' + str(k.get("score"))))
        per += (str(k.get('name')) + ' -- ' + str(k.get("score")) + '\n')
    bot.send_message(msg.chat.id, '___id___счёт___\n' + per)




    # рандомно выбираем из словоря результат и записываем

    # графика для пользователя

    # сравнение номера введенного пользователем резукльтата с записанным выше

    # вывод сообщения


if __name__ == '__main__':
    bot.polling(none_stop=True)


