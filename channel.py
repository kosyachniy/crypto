from func.main import *

trades = db['trade']

with open('data/set.txt', 'r', encoding='utf-8') as file:
	channeldeposit = json.loads(file.read())['default']['channeldeposit']

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
				formated += exchangers[i['exchanger']][0] + ' ' #' - '
			formated += '#%s ' % (currencies[i['currency']][1],)
			format2 = formated + ''
			if i['safe'] == 1:
				formated += '#надёжный'
				format2 += '#reliable'
			elif i['safe'] == -1:
				formated += '#рискованный'
				format2 += '#unreliable'
			if i['term'] == 0:
				formated += ' #краткосрочный'
				format2 += ' #short'
			elif i['term'] == 1:
				formated += ' #среднесрочный'
				format2 += ' #middle'
			elif i['term'] == 2:
				formated += ' #долгорочный'
				format2 += ' #long'

			pric = i['realprice']
			if not pric:
				pric = price(currencies[i['currency']][1])
			rub = stock[i['exchanger']].ru()
			usd = stock[i['exchanger']].us()
			if pric:
				formated += '\nɃ %.8f (%d₽)' % (pric, pric / rub)
				format2 += '\nɃ %.8f (%d$)' % (pric, pric / usd)
			formated += '\n--------------------\nПокупка:'
			format2 += '\n--------------------\nBuy:'
			if i['price']:
				if i['price'] > pric:
					formated += '\nɃ %.8f (отложенный ордер)' % pric
					format2 += '\nɃ %.8f (pending order)' % pric
				elif i['price'] < pric:
					formated += '\nɃ %.8f (ждём коррекции)' % pric
					format2 += '\nɃ %.8f (waiting for correction)' % pric

				pric = i['price']
			formated += '\nV %d%% от бюджета' % (i['volume'] * 100,)
			format2 += '\nV %d%% of the deposit' % (i['volume'] * 100,)
			if i['exchanger'] >= 0:
				balance = stock[i['exchanger']].info('') * channeldeposit * i['volume']
				if balance:
					formated += '\n%.8fɃ (%d₽)' % (balance, balance / rub)
					format2 += '\n%.8fɃ (%d$)' % (balance, balance / usd)

			first = 0
			if pric:
				if len(i['out']):
					formated += '\n\nНаша стратегия:' #Продажа
					format2 += '\n\nOur strategy:' #Sell
				for j in i['out']:
					x = j[2] if j[1] else pric * j[2]
					if not first: first = x
					formated += '\n%.8fɃ - %d%% от купленного' % (x, j[0] * 100)
					format2 += '\n%.8fɃ - %d%% of the purchased' % (x, j[0] * 100)
				x = i['loss'][1] if i['loss'][0] else pric * i['loss'][1]
				formated += '\n\nСтоп-цена: %.8fɃ' % x
				format2 += '\n\nStop-loss: %.8fɃ' % x

			send(formated, channelid)
			send(format2, twochannel)

			if pric and first >= i['realprice']:
				try:
					y = stock[excd if i['exchanger'] == -1 else i['exchanger']].last(i['currency'])
					minutes = graph(y, i['out'][0][2] if i['out'][0][1] else pric * i['out'][0][2])
					if minutes > 5:
						send('#'+currencies[i['currency']][1], [channelid, twochannel], 're.png')
				except:
					pass

if __name__ == '__main__':
	channel()