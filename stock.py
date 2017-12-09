from func.main import *

table = db['history']
settings = db['set']

'''
		if i['type'] == 'buy':
#Выставить покупку
			if not i['order']:

#Если покупка исполнена
			elif stock[i['exchanger']].order(i['order']):
'''

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())['default']
	timebuy = s['timebuy']
	timesell = s['timesell']
	timeloss = s['timeloss']

stamp = lambda x: mktime(strptime(x, '%d.%m.%Y %H:%M:%S')) // 60
now = lambda: mktime(gmtime()) // 60

def selll(i, sell):
	if not i['processed']:
		stock[i['exchanger']].cancel(i['order'])
		i['order'] = stock[i['exchanger']].trade(i['currency'], i['count'], sell, 1)
		i['price'] = sell
		#изменить тип на loss и отдельно отслеживать

		if i['order']:
			i['processed'] = 1
			rub = stock[i['exchanger']].ru()
			formated = 'Продать %s!\n-----\nК %.8f\nɃ %.8f (%d₽)\n∑ %.8f (%d₽)' % (currencies[i['currency']][1], i['count'], i['price'], i['price'] / rub, i['price'] * i['count'], (i['price'] * i['count']) / rub)
			send(formated)
		else:
			i['success'] = 2
			send('Ошибка продажи!')

	return i

while True:
	for i in table.find({'success': 0}):
#Если покупка исполнена
		if i['type'] == 'buy':
			if stock[i['exchanger']].order(i['order']):
				i['success'] = 1
				send('Покупка сработала №%d' % (i['message'],))
			else:
#Если покупка долго не исполняется
				if now() - stamp(i['time']) > timebuy:
					stock[i['exchanger']].cancel(i['order'])
					i['success'] = 2
					send('Вышло время на покупке №%d' % (i['message'],))

		elif i['type'] == 'sell':
#Если биткоин начал рост
			try:
				jump = settings.find_one({'name': 'jump'})['cont']
			except:
				jump = 0

			if jump == 1:
				sell = stock[i['exchanger']].price(i['currency'], 1)
				send('Начался рост биткоина!')
				i = selll(i, sell)

#Если продажа не выставлена
			if not i['order'] and table.find_one({'message': i['message'], 'type': 'buy'})['success']:
				i['order'] = stock[i['exchanger']].trade(i['currency'], i['count'], i['price'], 1)

				if i['order']:
					rub = stock[i['exchanger']].ru()
					formated = 'Продать %s!\n-----\nК %.8f\nɃ %.8f (%d₽)\n∑ %.8f (%d₽)' % (currencies[i['currency']][1], i['count'], i['price'], i['price'] / rub, i['price'] * i['count'], (i['price'] * i['count']) / rub)
					send(formated)
				else:
					send('Ошибка продажи!')
					i['success'] = 2

#Если продажа исполнена
			elif stock[i['exchanger']].order(i['order']):
				i['success'] = 1
				send('Продажа сработала №%d' % (i['message'],))
				#Выставление стоп-лосса на новый уровень
				for j in table.find({'message': i['message'], 'numsell': i['numsell']+1}):
					x = table.find_one({'message': i['message'], 'numsell': i['numsell']-1})
					j['loss'] = x['price'] if x else table.find_one({'message': i['message'], 'type': 'buy'})['price']
					table.save(j)

			else:
				sell = stock[i['exchanger']].price(i['currency'], 1)
#Если продажа долго не исполняется
				if now() - stamp(i['time']) > timesell:
					stock[i['exchanger']].cancel(i['order'])
					i['order'] = stock[i['exchanger']].trade(i['currency'], i['count'], stock[i['exchanger']].price(i['currency'], 1), 1)
					i['price'] = sell
					send('Вышло время на продаже №%d' % (i['message'],))
#Если стоп-лосс
				elif i['loss'] and now() - stamp(i['time']) >= timeloss:
					if type(sell) in (float, int) and sell < i['loss']:
						send('Сработал стоп-лосс на заказе №%d' % (i['message'],))
						i = selll(i, sell)

						#Остальные ордеры тоже снять
						for j in table.find({'message': i['message'], 'type': 'sell'}):
							j['loss'] = i['loss']
							table.save(j)

		table.save(i)