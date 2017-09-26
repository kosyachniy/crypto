from func import *

#Данные
botid = 356427214
channelid = -1001124440739
meid = 136563129

currencies = []
with open('data/currencies.txt', 'r') as file:
	for i in file:
		currencies.append(json.loads(i[:-1]))

transfers = [
	['BitCoin', 'BTC', 'Ƀ']
]
transfer = transfers[0][2]

exchanges = [
	['YObit'],
	['Bittrex'],
	['Poloniex']
]

vocabulary = {
	'buy': {'buy', 'купить', 'покупаем', 'докупаем', 'докупаемся', 'краткосрок', 'рост', 'среднесрочной'},
	'sell': {'sell', 'продать', 'продаём', 'продаем'}
}

url1 = 'https://ru.investing.com/crypto/currencies'
def price(x):
	print('!!!' + x) #
	page = requests.get(url1, headers={"User-agent": "Mozilla/5.0"}).text
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

#добавить актуальный перевод курса биткоинов
#url2 = 'https://yandex.ru/search/?text=btc%2Frub'
def ru():
	'''
	page = requests.get(url2).text
	soup = BeautifulSoup(page, 'lxml')
	inp = soup.find_all('input', class_='input__control')
	return int(inp[2]['value'].replace('\u2009', ''))
	'''
	return 226683

on = lambda text, words: any([word in text for word in words])

alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъёфывапролджэячсмитьбю'
clean = lambda cont: str(''.join([i if i in alphabet else ' ' for i in cont])).split()

while True:
#Список сообщений
	x = []
	with db:
		for i in db.execute("SELECT * FROM lastmessage"):
			chat, id = i
			text = ''

			try:
				text = bot.forward_message(meid, chat, id + 1).text
			except:
				try:
					text = bot.forward_message(meid, chat, id + 2).text
				except:
					id = 0
				else:
					id += 2
			else:
				id += 1

			if id:
				if text: #изображения
					x.append([chat, id, text.lower()])
				db.execute("UPDATE lastmessage SET message=(?) WHERE id=(?)", (id, chat))
			
			sleep(1)

	print(x)
	for i in x:
		buy = 0
		exc = 0
		cur = -1
		count = 1.0

#Распознание сигнала
		i_buy = on(i[2], vocabulary['buy'])
		i_sell = on(i[2], vocabulary['sell'])
		if i_buy and i_sell: continue

		if i_buy:
			buy = 2
		elif i_sell:
			buy = 1
		else:
			buy = 0

		for j in range(len(exchanges)):
			if exchanges[j][0].lower() in i[2]:
				exc = j
				break

		t = 0
		for j in range(1, len(currencies)):
			text = clean(i[2])
			#print(text)
			if currencies[j][1].lower() in text or currencies[j][0].lower() in text:
				print(j, currencies[j])
				if t == 0:
					t = 1
				elif t == 1:
					t = 2
					break

				cur = j
		if t == 2: continue #

		total = 0
		with db:
			for i in db.execute("SELECT * FROM currencies WHERE changer=(?) and currency=0", (exc,)):
				total = i[3]

		#убрать рассчёт доли при продаже
		print(total, cur, buy, exc)

		#постваить процент, после которого сделка совершится
		if buy or cur>=0:
#Определение количества
			operation = price(currencies[cur][1])
			delta = total * 0.03
			count = delta / operation

#Сборка сообщения на Telegram-канал
			if buy == 2:
				sign = '-'
			elif buy == 1:
				sign = '+'
			else:
				sign = '±'

			if buy == 2:
				buy = 'купить'
			elif buy == 1:
				buy = 'продать'
			else:
				buy = 'не определено'

			if cur == -1:
				cur1 = 'Криптовалюта не определена'
				cur2 = 'Индекс не определён'
			else:
				cur1 = currencies[cur][0]
				cur2 = currencies[cur][1]

			rub = ru()

			#T %d.%d %d:%d , day, month, hour, minute
			#exchanges[exc][0] + ' - ' if exc else ''
			formated = '%s (%s)\n%s%s\n--------------------\n∑ %f%s (%d₽)\nK %f\nΔ %s%f%s (%s%d₽)' % (cur1, buy, exchanges[exc][0] + ' - ', cur2, total, transfer, total * rub, count, sign, delta, transfer, sign, delta * rub)

			#бота перенести в отдельный файл
			bot.send_message(meid, formated)
			bot.forward_message(meid, chat, id)

			t = [''] * len(exchanges)
			btc = [0] * len(exchanges)
			with db:
				b = True
				co = 0
				for i in db.execute("SELECT * FROM currencies WHERE changer=(?) and currency=(?)", (exc, cur)):
					b = False
					co = i[2]
				print(exc, b, co)
				if b:
					db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (?, ?, ?, ?)", (cur, exc, count, delta))
				else:
					db.execute("UPDATE currencies SET count=(?) WHERE changer=(?) and currency=(?)", (count + co, exc, cur)) #добавить среднюю цену по валюте
				db.execute("UPDATE currencies SET count=(?) WHERE changer=(?) and currency=0", (total * 0.97, exc))

				for i in db.execute("SELECT * FROM currencies"):
					pri = i[3] * price(currencies[i[1]][1]) if i[1] != 0 else i[3]
					btc[i[2]] += pri
					t[i[2]] += '\n' + currencies[i[1]][1] + '	' + str(round(i[3], 6)) + '   |   ' + str(round(pri, 6)) + 'Ƀ   |   ' + str(int(pri * rub)) + '₽'

			for i in range(len(exchanges)):
				t[i] += '\n∑ %fɃ (%d₽)' % (round(btc[i], 6), int(btc[i] * rub))

			formated = 'Сводка\n--------------------\nYObit%s\n--------------------\nBittrex%s\n--------------------\nPoloniex%s' % (t[0], t[1], t[2])
			bot.send_message(meid, formated)
			bot.send_message(meid, '-----------------------------------')
			#запись в базу данных

			sleep(5)