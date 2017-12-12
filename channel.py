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
				formated += '\n%.8fɃ (%d₽)' % (pric, pric / rub)
				format2 += '\n%.8fɃ (%d$)' % (pric, pric / usd)
			formated += '\n--------------------\nПокупка:'
			format2 += '\n--------------------\nBuy:'
			if i['price']:
				pric = i['price']
				formated += '\nɃ %.8f (%d₽)' % (pric, pric / rub)
				format2 += '\nɃ %.8f (%d$)' % (pric, pric / usd)
			formated += '\nV %d%% от бюджета' % (i['volume'] * 100,)
			format2 += '\nV %d%% of the deposit' % (i['volume'] * 100,)

			if pric:
				if len(i['out']):
					formated += '\n\nНаша стратегия:' #Продажа
					format2 += '\n\nOur strategy:' #Sell
				for j in i['out']:
					formated += '\n%.8fɃ - %d%% от купленного' % (j[2] if j[1] else pric * j[2], j[0] * 100)
					format2 += '\n%.8fɃ - %d%% of the purchased' % (j[2] if j[1] else pric * j[2], j[0] * 100)
				formated += '\n\nСтоп-цена: %.8fɃ' % (i['loss'][1] if i['loss'][0] else pric * i['loss'][1],)
				format2 += '\n\nStop-loss: %.8fɃ' % (i['loss'][1] if i['loss'][0] else pric * i['loss'][1],)

			send(formated, channelid)
			send(format2, twochannel)

			if pric:
				try:
					#print('stock[' + str(excd if i['exchanger'] == -1 else i['exchanger']) + '].last(' + str(i['currency']) + ', ' + str(i['out'][0][2] if i['out'][0][1] else pric * i['out'][0][2]) + ')')
					minutes = stock[excd if i['exchanger'] == -1 else i['exchanger']].last(i['currency'], i['out'][0][2] if i['out'][0][1] else pric * i['out'][0][2])
					if minutes > 5:
						send('#'+currencies[i['currency']][1], [channelid, twochannel], 're.png')
				except:
					pass

if __name__ == '__main__':
	channel()