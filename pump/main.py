import telebot, json

@bot.message_handler(content_types=["text"])
def text(message):
	pump(message.text)

if __name__ == '__main__':
	bot.polling(none_stop=True)