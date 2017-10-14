import json, telebot

with open('data/set.txt', 'r') as file:
	token = json.loads(file.read())['token']
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def text(message):
	bot.send_message(136563129, message)
	print('-------------')
	print(message)

bot.polling(none_stop=True)