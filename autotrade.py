from func import *

def find(x, id):
	for i in x:
		if i[0] == id and i[3] == 'buy':
			return i[1]

#Не рассмотрен случай, если ордер на покупку не исполнился вовремя
while True:
	x = []
	with open('data/history.txt', 'r') as file:
		for i in file:
			x.append(json.loads(i))

	t = -1
	for i in range(len(x)):
		if not x[i][2]:
			#Если покупка исполнена
			if x[i][3] == 'buy' and stock[x[i][5]].order(x[i][1]) == x[i][0]:
				x[i][2] = 1
				t = x[i][0]
				bot.send_message(meid, 'Покупка сработала №%d' % (i[0],))
				#bot.send_message(soid, 'Покупка сработала №%d' % (i[0],))
			elif x[i][3] == 'sell' and not x[i][1] and find(x, x[i][0]):
				#выставлены продажи - сообщение
				x[i][1] = stock[x[i][5]].trade(x[i][4], x[i][7], x[i][6], 1)
			else:
				t = -1

			#Если стоп-лосс
			if x[i][9]:
				if stock[x[i][5]].price(x[i][4]) < x[i][9]:
					stock[x[i][5]].cancel(x[i][1])
					x[i][1] = stock[x[i][5]].trade(x[i][4], x[i][7], 0, 1)
					x[i][6] = 0
					bot.send_message(meid, 'Сработал стоп-лосс на заказе №%d' % (i[0],))
					#bot.send_message(soid, 'Сработал стоп-лосс на заказе №%d' % (i[0],))
					if i + 1 < len(x) and x[i+1][0] == x[i][0]:
						x[i+1][9] = x[i][9]

			#Если продажа исполнена

			if stock[x[i][5]].order(i[1]):
				x[i][2] = 1
				bot.send_message(meid, 'Продажа сработала №%d' % (i[0],))
				#bot.send_message(soid, 'Продажа сработала №%d' % (i[0],))
				#Выставление стоп-лосса на новый уровень
				if i + 1 < len(x) and x[i+1][0] == x[i][0]:
					x[i+1][9] = x[i-1][6]

	#Запись + обновлённые данные
	sleep(60) #