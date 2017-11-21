fix_price = 0.0006
delta_first = 1.4
delta_second = 0.75

from time import sleep, gmtime, mktime
import sys, re
from func.trade import stock

texted = lambda x: re.sub('[^a-z1234567890]', '', x)
minut = lambda: mktime(gmtime()) // 60

def pump(chat, text, exc=0):
	send = lambda x: bot.send_message(chat, x)

#Подготовка данных
	#запуск из терминала
	exc = int(exc) #
	text = texted(text)
	start = minut()

	#price = stock[exc].price(text)
	y = stock[0].trader.trades(cur, limit)[cur]
	price = y[0]['price']
	for i in y:
		if price > i['price']:
			price = i['price']

	try:
		volume = fix_price / price #stock[exc].info() * 0.5
	except:
		send('Ошибка сумм!')
		return 0

#Покупка
	order = stock[exc].trade(text, volume, price)
	send('%s\n%fɃ' % (order, price))

	while not stock[exc].order(order):
		sleep(1)
		if minut() - start >= 3:
			stock[exc].cancel(order)
			send('Не было куплено!')
			return 0

	#sleep(1)
	send('Успешно куплено!')

#Первая попытка продать
	start = minut()
	price *= delta_first
	order = stock[exc].trade(text, volume * 0.999999, price, 'sell')
	send('%s\n%fɃ' % (order, price))

	while True:
		if stock[exc].order(order):
			send('Успешно продано!')
			return 0
		else:
			if minut() - start >= 2:
#Вторая попытка продать
				stock[exc].cancel(order)

				price *= delta_second
				order = stock[exc].trade(text, volume * 0.999999, price, 'sell')
				send('%s\n%fɃ' % (order, price))

				send('Понижаем цену!')

				while True:
					if stock[exc].order(order):
						send('Успешно продано!')
						return 0
					else:
						if minut() - start >= 150:
							send('Не было продано!')
							return 0
						sleep(10)
			sleep(5)

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