import telebot
from telebot import types
import config
import sys
import io

bot = telebot.TeleBot(config.TOKEN)

tems = ["Бінарний Пошук", "Щось ще", "І ще щось"]


user_state = {}


@bot.message_handler(commands=['start'])
def star(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_help = types.KeyboardButton('Help')
    item_promlems = types.KeyboardButton('Почати вирішувати задачи')
    item_test = types.KeyboardButton("Протестувати код")

    markup.add(item_help, item_promlems, item_test)

    bot.send_message(message.chat.id, 'Привіт, {0.first_name}!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Протестувати код')
def start_test(message):
    user_state[message.chat.id] = "testing"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_start = types.KeyboardButton('Тестувати код')
    item_back = types.KeyboardButton('Назад до меню')
    markup.add(item_back, item_start)
    bot.send_message(message.chat.id, "Меню для тесту кода:", reply_markup=markup)


@bot.message_handler(
    func=lambda message: user_state.get(message.chat.id) == "testing" and message.text == 'Тестувати код')
def handle_code_input(message):
    bot.send_message(message.chat.id, "Введіть код для тесту:")


@bot.message_handler(
    func=lambda message: user_state.get(message.chat.id) == "testing" and message.text != 'Назад до меню')
def handle_code_execution(message):
    try:
        user_code = message.text
        output_stream = io.StringIO()
        sys.stdout = output_stream
        exec(user_code, globals(), locals())
        output = output_stream.getvalue()
        sys.stdout = sys.stdout

        bot.send_message(message.chat.id, "Результат выполнения:\n" + output)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка: " + str(e))


@bot.message_handler(func=lambda message: message.text == "Назад до меню")
def back_to_menu(message):
    user_state[message.chat.id] = None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_help = types.KeyboardButton('Help')
    item_promlems = types.KeyboardButton('Почати вирішувати задачи')
    item_test = types.KeyboardButton("Протестувати код")
    markup.add(item_help, item_promlems, item_test)
    bot.send_message(message.chat.id, "Добре, ось головне меню", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Help':
            bot.reply_to(message, 'Бог допоможе')
        elif message.text == 'Почати вирішувати задачи' or message.text == "Назад до вибору тем":
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
            item6 = types.KeyboardButton("Назад до вибору тем")
            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(message.chat.id, 'Ось задачі з цієї теми', reply_markup=markup)
        elif message.text == "Протестувати код":
            if user_state.get(message.chat.id) != "testing":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item_start = types.KeyboardButton('Тестувати код')
                item_back = types.KeyboardButton('Назад до меню')
                markup.add(item_back, item_start)
                bot.send_message(message.chat.id, "Меею для тесту кода:", reply_markup=markup)


bot.infinity_polling()
