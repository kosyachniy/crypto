#Торговля по сигналам
from func import *

from functrade import *
stock = [YoBit()]

def trade():
#Определение последней необработанной операции
	#Начинает с после следующей исполненной операции
	num = 0
	try:
		with open('data/history.txt', 'r') as file:
			for i in file:
				num = json.loads(i)[0]
	except:
		pass
	print(num) #

	while True:
#Подготовка операций к исполнению
		operation = []
		with open('data/trade.txt', 'r') as file: #Пока что операции не удаляются
			for i in file:
				cont = json.loads(i)
				if cont['id'] > num:
					print('!!!', cont['id'])
					operation.append(json.loads(i))
		
		if not len(operation):
			sleep(5)
			continue
		num = operation[-1]['id']

		for i in operation:
#Рассчёт основных параметров для биржи
			price = stock[i['exchanger']].price(i['currency'])
			print(price)
			if not price: continue #валюты нет или в малом объёме

			count = stock[i['exchanger']].info() * i['volume'] / price
			time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

			succ = 0
			#if stock[i['exchange']].trade(i['currency'], count, price, 2):
			#	succ = 1
			print('Купить %s!\n-----\nК %f\nɃ %f\n∑ %f' % (currencies[i['currency']][1], count, price, count * price)) #

			sett = [i['id'], succ, 'buy', i['currency'], i['exchanger'], price, count, time]
			print(sett)
			with open('data/history.txt', 'a') as file:
				print(json.dumps(sett), file=file)

			if succ:
				su = 0

				for j in i['out']:
					pric = price * j[2] if j[1] else j[2]
					coun = count * j[0]
					su += coun * pric

					succ = 0
					#if stock[i['exchange']].trade(i['currency'], coun, pric, 1):
					#	succ = 1
					
					print('Продать %s!\n-----\nК %f\nɃ %f\n∑ %f' % (currencies[i['currency']][1], coun, pric, pric * coun)) #

					sett = [i['id'], succ, 'sell', i['currency'], i['exchanger'], pric, coun, time]
					with open('data/history.txt', 'a') as file:
						print(json.dumps(sett), file=file)

				loss = (price - i['loss'][1]) * count if i['loss'][0] else price * count * (1 - i['loss'][1])
				print('Худший случай: -%fɃ\nЛучший случай: +%fɃ' % (loss, su - vol)) #
			else:
				print('Ошибка покупки!\n')

if __name__ == '__main__':
	trade()