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
			if not i[2]:
				x.append(i)

	for i in range(len(x)):
		if not x[i][1] and x[i][3] == 'sell':
			if stock[x[i][5]].order(find(x, x[i][0])):
				for j in x:
					if j[0] == x[i][0]:
						x[i][1] = stock[x[i][5]].trade(i[4], j[7], j[6], 1)
