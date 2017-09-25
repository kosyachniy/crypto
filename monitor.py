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

while True:
	buy = 0
	exc = 0

	buy = 2
	price = 0.00000062
	total = 0.02268417
	cur = 0
	exc = 1

#Сборка сигнала на Telegram-канал
	delta = str(price)
	if buy == 2:
		delta = '-' + delta
	elif buy != 1:
		delta = '±' + delta

	if buy == 2:
		buy = 'купить'
	elif buy == 1:
		buy = 'продать'
	else:
		buy = 'не определено'

	#постваить процент, после которого сделка совершится
	bot.send_message(136563129, '%s (%s)\n%s - %s\n----------\nΔ %s%s\n∑ %f%s' % (currencies[cur][0], buy, exchanges[exc][0], currencies[cur][1], delta, transfer, total, transfer)) #T %d.%d %d:%d , day, month, hour, minute #-1001124440739 #бота перенести в отдельный файл
	#запись в базу данных

	sleep(5)