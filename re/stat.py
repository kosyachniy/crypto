#CSV
import csv

def write(text, name='db', sign=','):
	with open(name+'.csv', 'a') as file:
		csv.writer(file, delimiter=sign, quotechar=' ', quoting=csv.QUOTE_MINIMAL).writerow(text)

import json
with open('../data/set.txt', 'r') as file:
	tags = json.loads(file.read())['read']['tags']
tag = {i: [0, 0] for i in tags}

#MongoClient
from pymongo import MongoClient

db = MongoClient()['crypto']
messages = db['messages']
#trade = db['trade']
history = db['history']

a = dict()

for i in history.find():
	try:
		a[i['message']][i['type']] = i['success']
	except:
		a[i['message']] = {i['type']: i['success']}

print(a)

write(['id', 'Тег', 'Сообщение', 'Итог', '?'])

for i in range(1, max(a)+1)[::-1]:
	try:
		for j in db['messages'].find({'id': i}):
			if a[i]['buy'] == 1:
				if a[i]['sell'] == 1:
					for u in history.find({'message': i, 'type': 'sell'}):
						for t in history.find({'message': i, 'type': 'buy'}):
							if u['price'] - t['price'] >= 0:
								x = 'Продано в плюс!'
							else:
								x = 'Продано в минус.'
				elif a[i]['sell'] == 2:
					x = 'Продано в минус.'
				else:
					x = 'Ордер на продаже'
			elif a[i]['buy'] == 2:
				x = 'Ошибка покупки'
			else:
				x = 'Ордер на покупке'

			#j['text'] = '\'' + j['text'].replace('\n', '\\n') + '\''

			l = ''
			for o in tags:
				if o in j['text'].lower():
					l = o
					break
			tag[l][1] += 1
			if x == 'Продано в плюс!':
				tag[l][0] += 1

			write([i, l, '"' + j['text'] + '"' if '\n' in j['text'] else j['text'], x, '+' if x == 'Продано в плюс!' else ' '])
			print(i, l, '.', a[i]['buy'], '-', a[i]['sell'])
	except:
		print(i, '. None')

for i in tag:
	print('%d%	%s' % (int(tag[i][0] / tag[i][1] * 100), i))