import telebot
import os
from retouch import geniously_thing

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))


@bot.message_handler(commands=['ooops'])
def start_message(message):
    bot.send_message(message.chat.id, 'Хаха братик вот тебе и троян закинули!!!! ЛОХ')


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    bot.send_message(message.chat.id, "Wait please...")
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    result = geniously_thing(downloaded_file)

    bot.send_photo(message.chat.id, result[0])



bot.polling()

