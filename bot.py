import telebot
from retouch import geniously_thing

bot = telebot.TeleBot("1313333867:AAGW0TdI6lw5p-tyo0M5KX0QI6TdSdahwWw")


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
    bot.send_message(message.chat.id, result[1])


bot.polling()

