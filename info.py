from func.main import *

while True:
	if gmtime().tm_hour == 20 + utc:
		for j in range(len(stock)):
			if j != 1: continue #Только Bittrex

			formated = exchanges[j][0] + '\n--------------------\n'
			s = 0
			x = []
			rub = stock[j].ru()

			for i in stock[j].trader.get_balances()['result']:
				sell = stock[j].price(i['Currency'], 1) * i['Balance']
				if sell:
					x.append([sell, i['Currency']])
					s += sell
			for i in sorted(x)[::-1]:
				formated += '%s 	%fɃ 	(%d₽)\n' % (i[1], i[0], i[0] / rub)

			formated += '--------------------\nИтог: %fɃ (%d₽)' % (s, s / rub)
			send(formated)

	sleep(3600)