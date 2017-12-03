from func.main import *

trades = db['trade']

from bs4 import BeautifulSoup
url = 'https://ru.investing.com/crypto/currencies'
def price(x):
	#print('---' + x)
	try:
		page = requests.get(url, headers={"User-agent": "Mozilla/5.0"}).text
		soup = BeautifulSoup(page, 'lxml')
		table = soup.find('table', id='top_crypto_tbl')
		tr = table.find_all('tr')
		for i in tr[1:]:
			td = i.find_all('td')

			name = td[2].text
			index = td[3].text
			price = td[8].text.replace('.', '').replace(',', '.')

			if index == x:
				print(name, index, price)
				return float(price)

	except:
		try:
			return stock[1].price(x)
		except:
			return 0.0

def channel():
#Первоначальные значения
	try:
		num = trades.find().sort('id', -1)[0]['id']
	except:
		num = 0

	while True:
		x = [i for i in trades.find({'id': {'$gt': num}})]

		if not len(x):
			sleep(5)
			continue

		num = x[-1]['id']

		for i in x:
			formated = '%s\n' % (currencies[i['currency']][0],)
			if i['exchanger'] != -1:
				formated += exchangers[i['exchanger']][0] + ' - '
			formated += '#%s' % (currencies[i['currency']][1],)
			if i['term'] == 0:
				formated += ' - краткосрочный'
			elif i['term'] == 1:
				formated += ' - среднесрочный'
			elif i['term'] == 2:
				formated += ' - долгорочный'
			pric = stock[i['exchanger']].price(i['currency']) if i['exchanger'] >= 0 else price(currencies[i['currency']][1])
			rub = stock[i['exchanger']].ru()
			if pric:
				formated += '\n%.8fɃ (%d₽)' % (pric, pric / rub)
			'''
			if total != -1:
				formated += '\n--------------------\n∑ %fɃ (%d₽)\nK %f\nΔ %s%fɃ (%s%d₽)' % (total, total / rub, count, sign, delta, sign, delta / rub)
			formated += '\n--------------------\n∑ %fɃ (%d₽)\nK %f\nΔ %s%fɃ (%s%d₽)' % (total, total / rub, count, sign, delta, sign, delta / rub)
			'''
			formated += '\n--------------------\nПокупка:'
			if i['price']:
				pric = i['price']
				formated += '\nɃ %.8f (%d₽)' % (pric, pric / rub)
			formated += '\nV %d%% от бюджета' % (i['volume'] * 100,) #\n↓ %s  str(i['loss'][1]) + 'Ƀ' if i['loss'][0] else str(int(i['loss'][1] * 100)) + '%'
			if len(i['out']):
				formated += '\n\nНаша стратегия:' #Продажа
			for j in i['out']:
				formated += '\n%.8fɃ - %d%% от купленного' % (j[2] if j[1] else pric * j[2], j[0] * 100)
			formated += '\n\nСтоп-цена: %.8fɃ' % (i['loss'][1] if i['loss'][0] else pric * i['loss'][1],)

			#send(i['mess'], i['chat'], channelid)
			send(formated, group=channelid)

			stock[i['exchanger']].last(i['currency'], i['out'][0][2] if i['out'][0][1] else pric * i['out'][2])
			send(open('re.png', 'rb'), group=channelid)

if __name__ == '__main__':
	channel()