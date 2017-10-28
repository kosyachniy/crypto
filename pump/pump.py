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
		volume = 0.0006 / price #stock[exc].info() * 0.95
	except:
		send('Ошибка!')
		return 0

	order = stock[exc].trade(text, volume, price)
	send('%s\n%fɃ' % (order, price))

	while not stock[exc].order(order):
		if gmtime().tm_min - start >= 1:
			stock[exc].cancel(order)
			send('Ошибка покупки!')
			return 0

	sleep(1)
	send('Успешно куплено!')

	price *= 1.2
	order = stock[exc].trade(text, volume * 0.999999, price, 'sell')
	send('%s\n%fɃ' % (order, price))

	while True:
		if stock[exc].order(order):
			send('Успешно продано!')
			return 0
		else:
			if gmtime().tm_min - start >= 60:
				return 0
			sleep(5)

if __name__ == '__main__':
	pump(sys.argv[1])