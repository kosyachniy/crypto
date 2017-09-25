import json, telebot, urllib

with open('set.txt', 'r') as file:
	token = json.loads(file.read())['token']
bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.send_message(message.chat.id, 'Hi!')

@bot.message_handler(content_types=['document', 'audio', 'photo', 'voice'])
def docs(message):
	pass

@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
	pass

#@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
@bot.message_handler(content_types=["text"])
def text(message):
	bot.send_message(message.chat.id, message.text)
	bot.send_message(-1001124440739, message.text)
	print(message.chat.id, message.forward_from_chat)

if __name__ == '__main__':
	bot.polling(none_stop=True)