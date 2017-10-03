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
					#print('!!!', currencies[cont['currency']][1])
					operation.append(json.loads(i))
		
		if not len(operation):
			sleep(5)
			continue
		num = operation[-1]['id']

		for i in operation:
#Рассчёт основных параметров для биржи
			if i['exchanger'] == -1: i['exchanger'] = 0 #Биржа по умолчанию
			i['exchanger'] = 0 #Временная замена на одну биржу

			price = stock[i['exchanger']].price(i['currency'])
			if not price: continue #валюты нет или в малом объёме

			delta = stock[i['exchanger']].info() * i['volume']
			if delta < stock[i['exchanger']].min:
				delta = stock[i['exchanger']].min
			price = delta / price

			#сделать проверку достаточно ли средств

			time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
			rub = stock[i['exchanger']].trader.ticker('btc_rur')['btc_rur']['buy']

#Покупка
			succ = stock[i['exchanger']].trade(i['currency'], count, price, 2)

			bot.forward_message(meid, i['chat'], i['mess'])
			bot.send_message(meid, 'Купить %s!\n-----\nК %.8f\nɃ %.8f (%d₽)\n∑ %.8f (%d₽)' % (currencies[i['currency']][1], count, price, price * rub, price * count, price * count * rub))

			sett = [i['id'], succ, 'buy', i['currency'], i['exchanger'], price, count, time]
			print(sett)
			with open('data/history.txt', 'a') as file:
				print(json.dumps(sett), file=file)

			#ждать исполнения ордеров

			if succ:
				su = 0

				for j in i['out']:
					pric = j[2] if j[1] else price * j[2]
					coun = count * j[0]
					su += coun * pric

					succ =  stock[i['exchanger']].trade(i['currency'], coun, pric, 1)

					#неправильное отображение цены в биткоинах
					bot.send_message(meid, 'Продать %s!\n-----\nК %.8f\nɃ %.8f (%d₽)\n∑ %.8f (%d₽)' % (currencies[i['currency']][1], coun, pric, pric * rub, pric * coun, pric * coun * rub))

					sett = [i['id'], succ, 'sell', i['currency'], i['exchanger'], pric, coun, time]
					with open('data/history.txt', 'a') as file:
						print(json.dumps(sett), file=file)

				vol = price * count
				loss = (price - i['loss'][1]) * count if i['loss'][0] else vol * (1 - i['loss'][1])
				bot.send_message(meid, 'Худший случай: -%fɃ (-%d₽)\nЛучший случай: +%fɃ (+%d₽)' % (loss, loss * rub, su - vol, (su - vol) * rub))
			else:
				print('Ошибка покупки!\n')
				bot.send_message(meid, 'Ошибка покупки!')
			bot.send_message(meid, '------------------------------')

if __name__ == '__main__':
	trade()