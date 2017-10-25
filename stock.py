from func.main import *

while True:
	for i in table.find({'success': 0}):
		#Если покупка исполнена
		if i['type'] == 'buy' and stock[i['exchanger']].order(i['order']):
			i['success'] = 1
			send('Покупка сработала №%d' % (i['message'],))
		
		elif i['type'] == 'sell':
			#Если продажа не выставлена
			if not i['order'] and table.find_one({'message': i['message'], 'type': 'buy'})['success']:
				i['order'] = stock[i['exchanger']].trade(i['currency'], i['count'], i['price'], 1)

				rub = stock[i['exchanger']].ru()
				formated = 'Продать %s!\n-----\nК %.8f\nɃ %.8f (%d₽)\n∑ %.8f (%d₽)' % (currencies[i['currency']][1], i['count'], i['price'], i['price'] / rub, i['price'] * i['count'], (i['price'] * i['count']) / rub)
				send(formated)

			#Если продажа исполнена
			elif stock[i['exchanger']].order(i['order']):
				i['success'] = 1
				send('Продажа сработала №%d' % (i['message'],))
				#Выставление стоп-лосса на новый уровень
				for j in table.find({'message': i['message'], 'numsell': i['numsell']+1}):
					x = table.find_one({'message': i['message'], 'numsell': i['numsell']-1})
					j['loss'] = x['price'] if x else table.find_one({'message': i['message'], 'type': 'buy'})['price']
					table.save(j)

			#Если стоп-лосс
			elif i['loss']:
				sell = stock[i['exchanger']].price(i['currency'], 1)
				if type(sell) in (float, int) and sell < i['loss']:
					stock[i['exchanger']].cancel(i['order'])
					i['order'] = stock[i['exchanger']].trade(i['currency'], i['count'], sell, 1)
					i['price'] = sell
					send('Сработал стоп-лосс на заказе №%d' % (i['message'],))

					if i['order']:
						rub = stock[i['exchanger']].ru()
						formated = 'Продать %s!\n-----\nК %.8f\nɃ %.8f (%d₽)\n∑ %.8f (%d₽)' % (currencies[i['currency']][1], i['count'], i['price'], i['price'] / rub, i['price'] * i['count'], (i['price'] * i['count']) / rub)
						send(formated)
					else:
						i['success'] = 2
						send('Ошибка продажи!')

					#Остальные ордеры тоже снять
					for j in table.find({'message': i['message'], 'type': 'sell'}):
						j['loss'] = i['loss']
						table.save(j)

		table.save(i)