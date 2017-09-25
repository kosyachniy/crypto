from func import *

currencies = [
	['DigitalNote', 'XDN'],
	[]
]

transfers = [
	['BitCoin', 'BTC', 'Ƀ']
]
transfer = transfers[0][2]

while True:
	buy = 2
	price = 0.00000062
	total = 0.02268417

	currency = currencies[0][1]
	buy = 'купить' if buy == 2 else 'продать' if buy == 1 else 'не определено'
	delta = '+' + str(price) if buy == 1 else str(price) if buy == 2 else '±' + str(price)

	#постваить процент, после которого сделка совершится
	bot.send_message(136563129, '%s (%s)\n----------\nΔ %s%s\n∑ %f%s' % (currency, buy, delta, transfer, total, transfer)) #T %d.%d %d:%d , day, month, hour, minute #-1001124440739 #бота перенести в отдельный файл
	#запись в базу данных

	sleep(5)