from time import sleep, gmtime

texted = lambda x: ''.join([i for i in x.lower() if i in 'qwertyuiopasdfghjklzxcvbnm.'])

#Биржи
from func.trade import stock
exc = 0

#Telegram
import telebot

token = '417063852:AAFvfJdVGgLv9odlnY_gaiMmV4NIBMlgvOQ'
meid = 136563129

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def text(message):
	text = texted(message.text)
	start = gmtime().tm_min

	price = stock[exc].price(text)
	volume = stock[exc].min / price #stock[exc].info() * 0.95
	order = stock[exc].trade(text, volume, price * 1.1)

	bot.send_message(meid, order)

	t = False
	while not t:
		if stock[exc].order(order):
			t = True
		elif gmtime().tm_min - start >= 5:
			stock[exc].cancel(order)
			break

	if t:
		sleep(1)
		bot.send_message(meid, 'Успешно куплено!')
		order = stock[exc].trade(text, volume * 0.999999, price * 1.5, 'sell')

		bot.send_message(meid, order)

		while True:
			if stock[exc].order(order):
				bot.send_message(meid, 'Успешно продано!')
				sleep(5)
	else:
		bot.send_message(meid, 'Ошибка покупки!')

if __name__ == '__main__':
	bot.polling(none_stop=True)