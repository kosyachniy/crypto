from func import *

#Данные
currencies = [
	['DigitalNote', 'XDN']
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

vocabulary = {
	'buy': {'buy', 'купить', 'покупаем'},
	'sell': {'sell', 'продать', 'продаём', 'продаем'},
	'buy': {'buy', 'купить', 'покупаем'},
	'buy': {'buy', 'купить', 'покупаем'},
}

on = lambda text, words: any([word in text for word in words])

def price(x):
	return [0.0000046, 0.00000062][x+1]

while True:
#Список сообщений
	x = []
	with db:
		for i in db.execute("SELECT * FROM lastmessage"):
			chat, id = i
			#id = 550 #
			text = ''

			try:
				text = bot.forward_message(136563129, chat, id + 1).text
			except:
				try:
					text = bot.forward_message(136563129, chat, id + 2).text
				except:
					id = 0
				else:
					id += 2
			else:
				id += 1

			if id:
				if text: #изображения
					x.append([chat, id, text.lower()])
				db.execute("UPDATE lastmessage SET message=(?) WHERE id=(?)", (id, chat))
			
			sleep(1)

	print(x)
	for i in x:
		buy = 0
		exc = -1
		cur = -1
		count = 1.0
		rub = price(-1)

#Распознание сигнала
		i_buy = on(i[2], vocabulary['buy'])
		i_sell = on(i[2], vocabulary['sell'])
		if i_buy and i_sell: continue

		if i_buy:
			buy = 2
		elif i_sell:
			buy = 1
		else:
			buy = 0

		for j in range(len(exchanges)):
			if exchanges[j][0].lower() in i[2]:
				exc = j
				break

		for j in range(len(currencies)):
			if currencies[j][1].lower() in i[2] or currencies[j][0].lower() in i[2]:
				cur = j
				break

		total = 0
		with db:
			for i in db.execute("SELECT * FROM currencies WHERE changer=(?) and currency=-1", (exc,)):
				total = i[3]

		#убрать рассчёт доли при продаже

#Определение количества
		operation = price(cur)
		delta = total * 0.03
		count = delta / operation

#Сборка сообщения на Telegram-канал
		if buy == 2:
			sign = '-'
		elif buy == 1:
			sign = '+'
		else:
			sign = '±'

		if buy == 2:
			buy = 'купить'
		elif buy == 1:
			buy = 'продать'
		else:
			buy = 'не определено'

		#постваить процент, после которого сделка совершится
		#проверка хватает ли денег
		bot.send_message(136563129, '%s (%s)\n%s - %s\n--------------------\n∑ %f%s (%d₽)\nK %f\nΔ %s%f%s (%s%d₽)' % (currencies[cur][0], buy, exchanges[exc][0], currencies[cur][1], total, transfer, total / rub, count, sign, delta, transfer, sign, delta / rub)) #T %d.%d %d:%d , day, month, hour, minute #-1001124440739 #бота перенести в отдельный файл
		bot.forward_message(136563129, chat, id + 2) #
		#запись в базу данных

		sleep(5)