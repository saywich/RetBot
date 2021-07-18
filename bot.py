import telebot
import random
from telebot import types
import os
from retouch import geniously_thing

bot = telebot.TeleBot(os.environ.get('__BOT_TOKEN__'))
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
paymentKeyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('⚫ ЧБ', '🟢 Инверсия')
keyboard1.row('🔴 Окраснить', '⚪ Осветлить')
keyboard1.row('🟦 Пиксели 🟦')
paymentKeyboard.row('проверить оплату')
PRICE = types.LabeledPrice(label='Фоточка', amount=10000)
INP_PATH = 'data/images/inputs'
RES_PATH = 'data/images/results'


def remove_files(files: list):
    for file in files:
        os.remove(file)


@bot.message_handler(commands=['ooops'])
def start_message(message):
    bot.send_message(message.chat.id, 'Хаха братик вот тебе и троян закинули!!!! ЛОХ')


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    bot.send_message(message.chat.id, 'акак', reply_markup=keyboard1)
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = f'{INP_PATH}/{message.chat.id}.png'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


@bot.message_handler(content_types=['text'])
def get_ret_mode(message):
    if message.text.upper() == '🟦 ПИКСЕЛИ 🟦':
        input_image = f'{INP_PATH}/{message.chat.id}.png'
        result_image = f'{RES_PATH}/{message.chat.id}.png'
        result = geniously_thing(input_image, result_image)
        if result[0]:
            with open(result_image, 'rb') as image:
                bot.send_photo(message.chat.id, image)
                bot.send_message(message.chat.id, result[1])
            remove_files([input_image, result_image])


bot.polling()

