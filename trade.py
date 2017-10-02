#Торговля по сигналам
from func import *

from functrade import *
stock = [YoBit()]

def trade():
	try:
		with open('data/history.txt', 'r') as file:
			num = json.loads(file.read()[-1])['id']
	except:
		num = 0

	while True:
		operation = []
		with open('data/trade.txt', 'r') as file: #Пока что операции не удаляются
			for i in file:
				cont = json.loads(i)
				if cont['id'] >= num:
					operation.append(json.loads(i))

		for i in operation:
			price = stock[i['exchange']].price(i['currency'])
			count = stock[i['exchange']].info() * i['volume'] / pricetime
			time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

			succ = 0
			if stock[i['exchange']].trade(i['currency'], count, price, 2):
				succ = 1

			sett = [num, succ, 'buy', i['currency'], i['exchanger'], time]
			with open('data/history.txt', 'a') as file:
					print(i, file=file)

			if succ:


				
