fix_price = 0.0006
delta = 1.4

from time import sleep #, gmtime
import sys, re
from func.trade import stock

texted = lambda x: re.sub('[^a-z]', '', x)

def pump(chat, text, exc=0):
	send = lambda x: bot.send_message(chat, x)

	#запуск из терминала
	exc = int(exc) #
	text = texted(text)
	#временное ограничение и продажа
	#start = gmtime().tm_min

	price = stock[exc].price(text) #

	try:
		volume = fix_price / price #stock[exc].info() * 0.5
	except:
		send('Ошибка сумм!')
		return 0

	order = stock[exc].trade(text, volume, price)
	send('%s\n%fɃ' % (order, price))

	while not stock[exc].order(order):
		sleep(1)
		'''
		if gmtime().tm_min - start >= 1:
			stock[exc].cancel(order)
			send('Ошибка покупки!')
			return 0
		'''

	#sleep(1)
	send('Успешно куплено!')

	price *= delta
	order = stock[exc].trade(text, volume * 0.999999, price, 'sell')
	send('%s\n%fɃ' % (order, price))

	while True:
		if stock[exc].order(order):
			send('Успешно продано!')
			return 0
		'''
		else:
			if gmtime().tm_min - start >= 60:
				return 0
			sleep(5)
		'''

#Telegram
import telebot

#заменить на основного бота
token = '417063852:AAFvfJdVGgLv9odlnY_gaiMmV4NIBMlgvOQ'

bot = telebot.TeleBot(token)

#заменить на изображение
@bot.message_handler(content_types=["text"])
def text(message):
	pump(message.chat.id, message.text)

if __name__ == '__main__':
	bot.polling(none_stop=True)