from func import *

while True:
	if gmtime().tm_hour == 21: #часовой пояс
		formated = 'Bittrex\n--------------------\n'
		s = 0
		x = []
		rub = stock[1].ru()

		for i in stock[1].trader.get_balances()['result']:
			sell = stock[1].price(i['Currency'], 1) * i['Balance']
			if sell:
				x.append([sell, i['Currency']])
				s += sell
		for i in sorted(x)[::-1]:
			formated += '%s 	%fɃ 	(%d₽)\n' % (i[1], i[0], i[0] / rub)

		formated += '--------------------\nИтог: %fɃ (%d₽)' % (s, s / rub)
		bot.send_message(meid, formated)
		bot.send_message(soid, formated)

	sleep(3600)