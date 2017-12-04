from func.main import *

days = db['days']
messages = db['messages']
history = db['history']

with open('data/set.txt', 'r') as file:
	excd = json.loads(file.read())['replacements']['exchanger']

stamp = lambda x: mktime(strptime(x, '%d.%m.%Y %H:%M:%S')) // 86400

#сделать регулярным по расписанию celery
if __name__ == '__main__':
	while True:
		if gmtime().tm_hour - utc in (6, 12, 20):
			for j in range(len(stock)):
				send(stock[j].all())

		if gmtime().tm_hour - utc == 17:
			now = mktime(gmtime()) // 86400

			try:
				i = days.find().sort('id', -1)[0]
			except:
				i = {'id': 0, 'sum': 10000}

			i['id'] += 1
			x = stock[excd].info()
			i['delta'] = i['sum'] - x
			if i['delta'] > 0:
				s = '+'
			elif i['delta'] < 0:
				s = '-'
				i['delta'] *= -1
			else:
				s = ''
			i['percent'] = i['delta'] * 100 / i['sum']
			i['sum'] = x
			i['signals'] = sum([1 for j in messages.find() if stamp(j['time']) == now])

			i['orders'] = 0
			i['plus'] = 0
			i['minus'] = 0
			i['success'] = 0
			i['bad'] = 0
			for j in history.find():
				if stamp(j['time']) == now:
					i['orders'] += 1
					if j['success'] == 1:
						i['success'] += 1
						if j['type'] == 'sell':
							u = history.find_one({'message': j['message'], 'type': 'buy'})
							if j['price'] - u['price'] > 0:
								i['plus'] += 1
							else:
								i['minus'] += 1
					elif j['success'] == 2:
						i['bad'] += 1
			days.insert(i)

			send('Добрый вечер!\nЗаканчивается %dй день и мы подводим #итоги:\n\nВсего было %d сигналов (%d ордеров)\nИз них %d прибыльных и %d убыточных\nЕщё не исполнилось %d ордеров.\n\nΔ %s%.8f (%s%.1f%)Ƀ∑ %.8fɃ' % (i['id'], i['signals'], i['orders'], i['plus'], i['minus'], i['orders'] - i['success'] - i['bad'], s, i['delta'], s, i['percent'], i['sum']), group=channelid)

		sleep(3600)