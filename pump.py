from time import sleep, gmtime
import sys

#Биржи
from func.trade import stock
exc = 0

from func.telegram import *

texted = lambda x: ''.join([i for i in x.lower() if i in 'qwertyuiopasdfghjklzxcvbnm.'])

def pump(text):
	text = texted(text)
	start = gmtime().tm_min

	price = stock[exc].price(text)

	try:
		volume = stock[exc].min / price #stock[exc].info() * 0.95
	except:
		send('Ошибка!')
		return 0

	order = stock[exc].trade(text, volume, price * 1.1)
	send(order)

	while not stock[exc].order(order):
		if gmtime().tm_min - start >= 5:
			stock[exc].cancel(order)
			send('Ошибка покупки!')
			return 0

	sleep(1)
	send('Успешно куплено!')
	order = stock[exc].trade(text, volume * 0.999999, price * 1.5, 'sell')
	send(order)

	while True:
		if stock[exc].order(order):
			send('Успешно продано!')
			sleep(5)

if __name__ == '__main__':
	pump(sys.argv[1])