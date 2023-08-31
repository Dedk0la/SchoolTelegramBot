import telebot
from telebot import types
import config
import sys

bot = telebot.TeleBot(config.TOKEN)

tems = ["Бінарний Пошук", "Щось ще", "І ще щось"]


@bot.message_handler(commands=['start'])
def star(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_help = types.KeyboardButton('Help')
    item_promlems = types.KeyboardButton('Почати вирішувати задачи')

    markup.add(item_help, item_promlems)

    bot.send_message(message.chat.id, 'Привіт, {0.first_name}!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Help':
            bot.reply_to(message, 'Бог допоможе')
        elif message.text == 'Почати вирішувати задачи':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Бінарний Пошук")
            item2 = types.KeyboardButton("Щось ще")
            item3 = types.KeyboardButton("І ще щось")
            item4 = types.KeyboardButton("Назад до меню")
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, 'Виберіть тему', reply_markup=markup)
        elif message.text == "Назад до меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_help = types.KeyboardButton('Help')
            item_promlems = types.KeyboardButton('Почати вирішувати задачи')
            markup.add(item_help, item_promlems)

            bot.send_message(message.chat.id, 'Добре, ось головне меню', reply_markup=markup)
        elif message.text in tems:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Задача №1")
            item2 = types.KeyboardButton("Задача №2")
            item3 = types.KeyboardButton("Задача №3")
            item4 = types.KeyboardButton("Задача №4")
            item5 = types.KeyboardButton("Назад до меню")
            markup.add(item1, item2, item3, item4, item5)

            bot.send_message(message.chat.id, 'Ось задачі з ціеї теми', reply_markup=markup)


bot.infinity_polling()
