from func import *

#Данные
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

while True:
#Список сообщений
	x = []
	with db:
		for i in db.execute("SELECT * FROM lastmessage"):
			chat, id = i
			#id = 605 #
			text = ''

			try:
				text = bot.forward_message(136563129, chat, id + 1).text
			except:
				try:
					text = bot.forward_message(136563129, chat, id + 2).text
				except:
					pass
				else:
					id += 2
			else:
				id += 1

			x.append([chat, id, text])
			#db.execute("UPDATE lastmessage SET message=(?) WHERE id=(?)", (id, chat))
			sleep(1)
	with db:
		for i in x:
			db.execute("UPDATE lastmessage SET message=(?) WHERE id=(?)", (i[1], i[0]))

	print(x)
	'''
	buy = 0
	exc = 0
	count = 1.0
	rub = price(-1)

#Распознание сигнала
	buy = 2
	total = 0.02268417
	cur = 0
	exc = 1

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
	bot.forward_message(136563129, chat, id + 2)
	#запись в базу данных
	'''
	sleep(5)
	with db:
		for i in db.execute("SELECT * FROM lastmessage"):
			print(i)