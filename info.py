from func.main import *

days = db['days']
messages = db['messages']
history = db['history']

with open('data/set.txt', 'r') as file:
	excd = json.loads(file.read())['replacements']['exchanger'] + 0 #?

stamp = lambda x: mktime(strptime(x, '%d.%m.%Y %H:%M:%S')) // 86400

def end(x):
	if x % 10 == 1 and x != 11:
		return ''
	elif x % 10 in (2, 3, 4) and x not in (12, 13, 14):
		return 'а'
	return 'ов'

def end2(x):
	if x % 10 == 1 and x != 11:
		return 'ый'
	return 'ых'

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
				del i['_id']
			except:
				i = {'id': 0, 'sumrub': 10000, 'sumbtc': 0.015}

			i['id'] += 1
			x = stock[excd].info()
			xrub = x / stock[excd].ru()
			i['signals'] = sum([1 for j in messages.find() if stamp(j['time']) == now])

			i['delta'] = x - i['sumbtc']
			if i['delta'] > 0:
				s1 = '+'
			elif i['delta'] < 0:
				s1 = '-'
				i['delta'] *= -1
			else:
				s1 = ''
			i['percent'] = i['delta'] * 100 / i['sumbtc']
			i['sumbtc'] = x

			i['deltarub'] = xrub - i['sumrub']
			if i['deltarub'] > 0:
				s2 = '+'
			elif i['deltarub'] < 0:
				s2 = '-'
				i['deltarub'] *= -1
			else:
				s2 = ''
			i['percentrub'] = i['deltarub'] * 100 / i['sumrub']
			i['sumrub'] = xrub

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

			text = 'Добрый вечер!\nИтак, заканчивается %dй день и мы подводим #итоги:\n\nВсего было %d сигнал%s (%d ордер%s)\nИз них %d прибыльн%s и %d убыточн%s.' % (i['id'], i['signals'], end(i['signals']), i['orders'], end(i['orders']), i['plus'], end2(i['plus']), i['minus'], end2(i['minus']))
			if i['orders'] - i['success'] - i['bad']:
				text += '\nЕщё не исполнилось %d ордеров.' % (i['orders'] - i['success'] - i['bad'],)
			text += '\n\nΔ %s%.6fɃ (%s%.1f%%)\nΔ %s%d₽ (%s%.1f%%)\n\n∑ %.6fɃ (%d₽)' % (s1, i['delta'], s1, i['percent'], s2, i['deltarub'], s2, i['percentrub'], i['sumbtc'], i['sumrub'])
			send(text, group=channelid)

		sleep(3600)