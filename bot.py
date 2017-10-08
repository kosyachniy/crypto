from func import *

from functrade import *
stock = [YoBit()]

url = 'https://ru.investing.com/crypto/currencies'
def price(x):
	print('!!!' + x) #
	page = requests.get(url, headers={"User-agent": "Mozilla/5.0"}).text
	soup = BeautifulSoup(page, 'lxml')
	table = soup.find('table', id='top_crypto_tbl')
	tr = table.find_all('tr')
	for i in tr[1:]:
		td = i.find_all('td')

		name = td[1].text
		index = td[2].text
		price = td[7].text.replace('.', '').replace(',', '.')
		
		if index == x:
			print(name, index, price)
			return float(price)

ru = lambda: float(requests.get('https://blockchain.info/tobtc?currency=RUB&value=1000').text) / 1000

def bott():
	#сделать контроль последнего обработанного id

	num = 0
	try:
		with open('data/trade.txt', 'r') as file:
			for i in file:
				num = json.loads(i)['id']
	except:
		pass

	#num = 0

	while True:
		operation = []
		with open('data/trade.txt', 'r') as file:
			for i in file:
				x = json.loads(i)
				if x['id'] > num:
					operation.append(x)
					num = x['id']

		rub = ru()
		for i in operation:
			formated = '%s\n'  % (currencies[i['currency']][0],)
			if i['exchanger'] != -1:
				formated += exchanges[i['exchanger']][0] + ' - '
			formated += currencies[i['currency']][1]
			if i['term'] == 0:
				formated += ' - краткосрочный'
			elif i['term'] == 1:
				formated += ' - среднесрочный'
			elif i['term'] == 2:
				formated += ' - долгорочный'
			pric = stock[i['exchanger']].price(i['currency']) if i['exchanger'] >= 0 else price(currencies[i['currency']][1])
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
				formated += '\n\nПродажа:'
			for j in i['out']:
				formated += '\n%.8fɃ - %d%% от купленного' % (j[2] if j[1] else pric * j[2], j[0] * 100) #(j[0] * 100, str(j[2]) + 'Ƀ' if j[1] else '+' + str(round((j[2] - 1) * 100)) + '%') #
			formated += '\n\nСтоп-цена: %.8fɃ' % (i['loss'][1] if i['loss'][0] else pric * i['loss'][1],)

			bot.forward_message(channelid, i['chat'], i['mess'])
			bot.send_message(channelid, formated)

if __name__ == '__main__':
	bott()

'''
			if total != -1:
#Сводка
				t = [i[0] for i in exchanges]
				btc = [0] * len(exchanges)
				for i in db.execute("SELECT * FROM currencies WHERE succ!=0 and changer=0"): #последние условие, т.к. другие биржи ещё не работают
					pric = stock[i[2]].price(i[1], 1) #
					pri = i[3] * pric if i[1] != 0 else i[3]
					print('---', i[4], pric)
					btc[i[2]] += pri
					rise = '↑ ' if pric - i[4] > 0 else '↓ ' if pric - i[4] < 0 else ''
					t[i[2]] += '\n%s%s	%.6f   |   %.6fɃ   |   %d₽' % (rise, currencies[i[1]][1], i[3], pri, pri / rub)

				for i in range(len(exchanges)):
					t[i] += '\n∑ %fɃ (%d₽)' % (round(btc[i], 6), int(btc[i] / rub))
				formated = 'Сводка\n--------------------\n%s' % (t[0],)
				bot.send_message(sendid, formated)
		elif buy >= 1:
			bot.send_message(sendid, 'Не распознано')
			bot.forward_message(sendid, chat, id)
		bot.send_message(sendid, '------------------------------')
'''