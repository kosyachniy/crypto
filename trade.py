#Торговля по сигналам
from func.main import *

trades = db['trade']
table = db['history']

def trade():
#Первоначальные значения
	try:
		num = trades.find().sort('id', -1)[0]['id'] + 1
	except:
		num = 0

	while True:
		x = [i for i in trades.find({'id': {'$gte': num-1}})]

		for i in x:
#Рассчёт основных параметров для биржи
			#if i['exchanger'] == -1: i['exchanger'] = 1 #Биржа по умолчанию
			i['exchanger'] = 1 #Временная замена на одну биржу

			#i['price'] = 0 #чтобы не заморачиваться и каждый раз быстро вводить покупку #теперь вводим 0.0
			price = i['price'] if i['price'] else stock[i['exchanger']].price(i['currency'])
			if not price: continue #валюты нет или в малом объёме

			#i['volume'] = 0.5 #
			delta = 0.001 #stock[i['exchanger']].info() * i['volume']
			if delta < stock[i['exchanger']].min:
				delta = stock[i['exchanger']].min
			count = delta / price

			#сделать проверку достаточно ли средств

			time = strftime('%d.%m.%Y %H:%M:%S')
			rub = stock[i['exchanger']].ru()

#Покупка
			succ = stock[i['exchanger']].trade(i['currency'], count, price, 2)

			send(i['mess'], forward=i['chat'])

			formated = 'Купить %s!\n-----\nК %.8f\nɃ %.8f (%d₽)\n∑ %.8f (%d₽)' % (currencies[i['currency']][1], count, price, price / rub, price * count, (price * count) / rub)
			send(formated)

			if succ:
				sett = {'message': i['id'], 'success': 0, 'order': succ, 'type': 'buy', 'currency': i['currency'], 'exchanger': i['exchanger'], 'price': price, 'count': count, 'time': time}
				print(sett)
				table.insert(sett)

#Продажа
				su = 0

				x = []
				for j in range(1, len(i['out']) + 1):
					#Если слишком маленький объём продажи
					#может ли быть такое, что все кроме первого объединятся, а первый будет слишком маленький
					pric = i['out'][-j][2] if i['out'][-j][1] else price * i['out'][-j][2]
					coun = count * i['out'][-j][0]
					print('!!!COUN!!!', coun * pric)
					if coun * pric < stock[i['exchanger']].min:
						i['out'][-1-j][0] += i['out'][-j][0]
						continue

					su += coun * pric

					succ = 0 #stock[i['exchanger']].trade(i['currency'], coun, pric, 1)

					x.append({'message': i['id'], 'success': 0, 'order': succ, 'type': 'sell', 'currency': i['currency'], 'exchanger': i['exchanger'], 'price': pric, 'count': coun, 'time': time})

				for j in range(len(x)-1):
					x[j]['loss'] = 0
				x[len(x)-1]['loss'] = i['loss'][1] if i['loss'][0] else i['loss'][1] * price
				
				for j in range(1, len(x)+1):
					x[-j]['numsell'] = j
					table.insert(x[-j])

#Худший - лучший случай
				vol = price * count
				loss = (price - i['loss'][1]) * count if i['loss'][0] else vol * (1 - i['loss'][1])
				formated = 'Худший случай: -%fɃ (-%d₽)\nЛучший случай: +%fɃ (+%d₽)' % (loss, loss / rub, su - vol, (su - vol) / rub)
				send(formated)
			else:
				print('Ошибка покупки!\n')
				send('Ошибка покупки!')
			send('------------------------------')

if __name__ == '__main__':
	trade()