import json, telebot, urllib

with open('set.txt', 'r') as file:
	token = json.loads(file.read())['token']
bot=telebot.TeleBot(token)

def telegram(x):
	@bot.message_handler(commands=['start', 'help'])
	def start(message):
		bot.send_message(message.chat.id, 'Hi!')

	@bot.message_handler(regexp="SOME_REGEXP")
	def handle_message(message):
		pass

	@bot.message_handler(content_types=["text"])
	def text(message):
		for i in range(len(x)):
			if x[i][0] == 1:
				x[i][0] = 0
				bot.send_message(-1001124440739, 'BitCoin\n----------\nΔ +%f$\nT %d.%d %d:%d' % x[i][1:])

		#bot.send_message(message.chat.id, message.text)
		#delta, day, month, hour, minute
		print(message.chat.id, message.forward_from_chat)

#if __name__ == '__main__':
	bot.polling(none_stop=True)