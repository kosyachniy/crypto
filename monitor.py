from func import *

currencies = [
	['DigitalNote', 'XDN'],
	[]
]

transfers = [
	['BitCoin', 'BTC', 'Ƀ']
]
transfer = transfers[0][2]

exchanges = [
	['YObit'],
	['Bittrex'],
	['Poloniex']
]

def price(x):
	return [0.0000046, 0.00000062][x+1]

medium = 0.0023

while True:
	buy = 0
	exc = 0
	count = 1.0
	rub = price(-1)

	buy = 2
	total = 0.02268417
	cur = 0
	exc = 1

	operation = price(cur)
	count = medium / operation

#Сборка сообщения на Telegram-канал
	operation = operation * count
	delta = str(operation)
	if buy == 2:
		delta = '-' + delta
	elif buy == 1:
		delta = '+' + delta
	else:
		delta = '±' + delta

	if buy == 2:
		buy = 'купить'
	elif buy == 1:
		buy = 'продать'
	else:
		buy = 'не определено'

	#постваить процент, после которого сделка совершится
	#проверка хватает ли денег
	bot.send_message(136563129, '%s (%s)\n%s - %s\n----------\n∑ %f%s (%f₽)\nK %f\nΔ %s%s(%f₽)' % (currencies[cur][0], buy, exchanges[exc][0], currencies[cur][1], total, transfer, total / rub, count, delta, transfer, operation / rub)) #T %d.%d %d:%d , day, month, hour, minute #-1001124440739 #бота перенести в отдельный файл
	#запись в базу данных

	sleep(5)