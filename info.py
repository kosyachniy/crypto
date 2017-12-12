from func.main import *

days = db['days']
messages = db['messages']
history = db['history']
bit = db['bit']
settings = db['set']

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())['default']
	jumpup = s['jumpup']
	jumpdown = s['jumpdown']
	channeldeposit = s['channeldeposit']

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

def end3(x):
	if x % 10 == 1 and x != 11:
		return 'лся'
	return 'лось'

def emd5(x):
	if x % 10 == 1 and x != 11:
		return ''
	return 'о'

end4 = lambda x: 's' if x != 1 else ''

#сделать регулярным по расписанию celery
if __name__ == '__main__':
	while True:
		tim = gmtime().tm_hour - utc
#Сводка балансов
		if tim in (6, 12, 20):
			for j in range(len(stock)):
				send(stock[j].all())

#Сводка дня в каналы
		if tim == 17:
			now = mktime(gmtime()) // 86400

			try:
				i = days.find().sort('id', -1)[0]
				del i['_id']
			except:
				i = {'id': 0, 'sumrub': 7735, 'sumbtc': 0.011407, 'sumusd': 100} #8000 0.12

			i['id'] += 1
			x = stock[excd].info('') * channeldeposit
			xrub = x / stock[excd].ru()
			xusd = x / stock[excd].us()
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

			i['deltausd'] = xusd - i['sumusd']
			if i['deltausd'] > 0:
				s3 = '+'
			elif i['deltausd'] < 0:
				s3 = '-'
				i['deltausd'] *= -1
			else:
				s3 = ''
			i['percentusd'] = i['deltausd'] * 100 / i['sumusd']
			i['sumusd'] = xusd

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
			orders = i['plus'] + i['minus'] + i['orders'] - i['success'] - i['bad']

			text = 'Добрый вечер!\nИтак, заканчивается %dй день и мы подводим #итоги:\n\nВсего был%s %d сигнал%s (%d ордер%s)\nИз них %d прибыльн%s и %d убыточн%s.' % (i['id'], end5(i['signals']), i['signals'], end(i['signals']), orders, end(orders), i['plus'], end2(i['plus']), i['minus'], end2(i['minus']))
			notclosed = i['orders'] - i['success'] - i['bad']
			if notclosed:
				text += '\nЕщё не исполни%s %d ордер%s.' % (end3(notclosed), notclosed, end(notclosed))
			text += '\n\nΔ %s%.6fɃ (%s%.1f%%)\nΔ %s%d₽ (%s%.1f%%)\n\n∑ %.6fɃ (%d₽)' % (s1, i['delta'], s1, i['percent'], s2, i['deltarub'], s2, i['percentrub'], i['sumbtc'], i['sumrub'])

			text2 = 'Good evening, guys!\nIt\'s our day\'s #results (day %d)\n\nIn total: %d signal%s (%d order%s)\n%d profit order%s & %d not-profit order%s.' % (i['id'], i['signals'], end4(i['signals']), orders, end4(orders), i['plus'], end4(i['plus']), i['minus'], end4(i['minus']))
			if notclosed:
				text2 += '\n%d order%s in process.' % (notclosed, end4(notclosed))
			text2 += '\n\nΔ %s%.6fɃ (%s%.1f%%)\nΔ %s%d$ (%s%.1f%%)\n\n∑ %.6fɃ (%d$)' % (s1, i['delta'], s1, i['percent'], s3, i['deltausd'], s3, i['percentusd'], i['sumbtc'], i['sumusd'])

			send(text, to=channelid)
			send(text2, to=twochannel)

#Изменение курсов
		i = settings.find_one({'name': 'jump'})
		try:
			if i['cont']: pass
		except:
			i = {'name': 'jump', 'cont': 0}

		ch = 1 / stock[excd].us()
		try:
			x = bit.find().sort('id', -1)
			num = x[0]['id']
			one = x[0]['cont']
		except:
			up = low = ch
			num = 0
		else:
			try:
				up = x[2]['cont']
			except:
				up = ch

			try:
				low = x[4]['cont']
			except:
				low = ch

		if ch / up >= jumpup or ch / one >= jumpup:
			if i['cont'] != 1:
				text = '#ВБиток\nРост биткоина +%d%% за 3 часа и +%d%% за час.\nПродавайте альткоины!' % (100 * (ch / up - 1), 100 * (ch / one - 1))
				text2 = '#toBTC\nBitCoin increased by +%d%% in 3 hours and +%d%% in one hour.\nSell altcoins!' % (100 * (ch / up - 1), 100 * (ch / one - 1))
				send(text, to=channelid)
				send(text2, to=twochannel)
				i['cont'] = 1

		elif ch / low <= jumpdown or ch / one <= jumpdown:
			if i['cont'] != 2:
				text = '#ВАльты\nПадение биткоина -%d%% за 5 часов и -%d%% за час.' % ((100 * (1 - ch / low)), (100 * (1 - ch / one)))
				text2 = '#toAlt\nBitCoin falling -%d%% in 5 hours and -%d%% in one hour.' % ((100 * (1 - ch / low)), (100 * (1 - ch / one)))
				send(text, to=channelid)
				send(text2, to=twochannel)
				i['cont'] = 2
		else:
			i['cont'] = 0

		bit.insert({'id': num+1, 'cont': ch})
		if '_id' in i: #
			settings.save(i)
		else:
			settings.insert(i)

		sleep(3600)