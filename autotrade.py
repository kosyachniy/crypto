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
			x.append(i)

	num = -1
	for i in range(len(x)):
		if not x[i][2]:
			#Если ордеры на продажу не были выставлены
			if not x[i][1] and x[i][3] == 'sell' and  stock[x[i][5]].order(find(x, x[i][0])):
				x[i][1] = stock[x[i][5]].trade(x[i][4], x[i][7], x[i][6], 1)

			#Если стоп-лосс
			if x[i][9]:
				if stock[x[i][5]].price(x[i][4]) < x[i][9]:
					stock[x[i][5]].cancel(x[i][1])
					stock[x[i][5]].trade(x[i][4], x[i][7], x[i][9], 1)
					if i + 1 < len(x) and x[i+1][0] == x[i][0]:
						x[i+1][9] = x[i][9]
						num = x[i][0]
				else:
					num = -1
			elif num == i[0]:
				stock[x[i][5]].cancel(i[1])
				stock[x[i][5]].trade(i[4], i[7], i[9], 1)
			else:
				num = -1

			#