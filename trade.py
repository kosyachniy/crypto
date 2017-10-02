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
			if not price: continue #валюты нет или в малом объёме

			count = stock[i['exchange']].info() * i['volume'] / price
			time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

			succ = 0
			#if stock[i['exchange']].trade(i['currency'], count, price, 2):
			#	succ = 1
			print('Купить %s!\n-----\nК %f\nɃ %f\n∑ %f' % (currencies[i['currency']], count, price, count * price)) #

			sett = [num, succ, 'buy', i['currency'], i['exchanger'], time]
			with open('data/history.txt', 'a') as file:
					print(i, file=file)

			if succ:
				su = 0

				for j in i['out']:
					pric = price * j[2] if j[1] else j[2]
					coun = count * j[0]
					su += coun * pric

					succ = 0
					#if stock[i['exchange']].trade(i['currency'], coun, pric, 1):
					#	succ = 1
					
					print('Продать %s!\n-----\nК %f\nɃ %f\n∑ %f' % (currencies[i['currency']], coun, pric, pric * coun)) #

					sett = [num, succ, 'sell', i['currency'], i['exchanger'], time]
					with open('data/history.txt', 'a') as file:
							print(i, file=file)

				loss = (price - i['loss'][1]) * count if i['loss'][0] else price * count * (1 - i['loss'][1])
				print('Худший случай: -%fɃ\nЛучший случай: +%fɃ' % (loss, su - vol)) #
			else:
				print('Ошибка покупки! %s' % (currencies[i['currency']],))