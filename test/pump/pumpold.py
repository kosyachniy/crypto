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

	try:
		volume = 0.002 / price #stock[exc].info() * 0.95
	except:
		bot.send_message(meid, 'Ошибка!')
		return 0

	order = stock[exc].trade(text, volume, price * 1.01)
	bot.send_message(meid, order)

	while not stock[exc].order(order):
		if gmtime().tm_min - start >= 5:
			stock[exc].cancel(order)
			bot.send_message(meid, 'Ошибка покупки!')
			return 0

	sleep(1)
	bot.send_message(meid, 'Успешно куплено!')
	order = stock[exc].trade(text, volume * 0.999999, price * 1.4, 'sell')
	bot.send_message(meid, order)

	while True:
		if stock[exc].order(order):
			bot.send_message(meid, 'Успешно продано!')
			return 0
			sleep(5)

if __name__ == '__main__':
	bot.polling(none_stop=True)