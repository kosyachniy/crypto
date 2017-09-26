#Контроль сигналов
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
	'buy': {'buy', 'купить', 'покупаем', 'покупка', 'докупаем', 'докупаемся', 'краткосрок', 'рост', 'среднесрочной'},
	'sell': {'sell', 'продать', 'продаём', 'продаем', 'продажа'}
}

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

def ru():
	return float(requests.get('https://blockchain.info/tobtc?currency=RUB&value=1000').text) / 1000

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
		if on(i[2], vocabulary['buy']):
			buy = 2
		elif on(i[2], vocabulary['sell']):
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

		if buy or cur>=0:
#Определение количества
			operation = price(currencies[cur][1])
			count = 0
			delta = 0
			if buy==1:
				with db:
					for j in db.execute("SELECT * FROM currencies WHERE currency=(?)", (cur,)):
						count += j[3]
						delta += count * operation
			else:
				delta = total * 0.03
				count = delta / operation
		else:
			continue

		if (buy != 1 and total > 0) or (buy == 1 and count > 0):
#Сборка сообщения на Telegram-канал
			sign = '±+-'[buy]
			buys = ['не определено', 'продать', 'купить'][buy]

			if cur == -1:
				cur1 = 'Криптовалюта не определена'
				cur2 = 'Индекс не определён'
			else:
				cur1 = currencies[cur][0]
				cur2 = currencies[cur][1]

			rub = ru()

			#T %d.%d %d:%d , day, month, hour, minute
			#exchanges[exc][0] + ' - ' if exc else ''
			formated = '%s (%s)\n%s%s\n--------------------\n∑ %f%s (%d₽)\nK %f\nΔ %s%f%s (%s%d₽)' % (cur1, buys, exchanges[exc][0] + ' - ' if buy != 1 else '', cur2, total, transfer, total / rub, count, sign, delta, transfer, sign, delta / rub)

			#бота перенести в отдельный файл
			bot.send_message(channelid, formated)
			bot.forward_message(channelid, chat, id)

			t = [i[0] for i in exchanges]
			btc = [0] * len(exchanges)
			time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
			with db:
#Добавление операции
				if buy != 1:
					db.execute("INSERT INTO currencies (currency, changer, count, price, loss, half, full, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (cur, exc, count, operation, operation * 0.9, operation * 1.05, operation * 1.1, time))
					db.execute("UPDATE currencies SET count=(?) WHERE changer=(?) and currency=0", (total * 0.97, exc))
				else:
					sell = [0] * len(exchanges)
					for j in db.execute("SELECT * FROM currencies WHERE currency=(?)", (cur,)):
						sell[j[2]] += j[3]
						db.execute("DELETE FROM currencies WHERE id=(?)'", (j[0],))
					for j in db.execute("SELECT * FROM currencies WHERE currency=0", (cur,)):
						db.execute("UPDATE currencies SET count=(?) WHERE changer=(?) and currency=0", (sell[j[2]] * operation + j[3], j[2]))

#Сводка
				for i in db.execute("SELECT * FROM currencies"):
					pric = price(currencies[i[1]][1])
					pri = i[3] * pric if i[1] != 0 else i[3]
					btc[i[2]] += pri
					rise = '↑ ' if i[4] - pric > 0 else '↓ ' if i[4] - pric < 0 else ''
					t[i[2]] += '\n' + rise + currencies[i[1]][1] + '	' + str(round(i[3], 6)) + '   |   ' + str(round(pri, 6)) + 'Ƀ   |   ' + str(int(pri / rub)) + '₽'
					'''
					if i[1] != 0:
						t[i[2]] += '   |   ' + str(i[5]) + '   |   ' + str(i[6]) + '   |   ' + str(i[7]) + '   |   ' + str(i[8])
					'''

			for i in range(len(exchanges)):
				t[i] += '\n∑ %fɃ (%d₽)' % (round(btc[i], 6), int(btc[i] / rub))

			formated = 'Сводка\n--------------------\n%s\n--------------------\n%s\n--------------------\n%s' % (t[0], t[1], t[2])
			bot.send_message(channelid, formated)
			bot.send_message(channelid, '-----------------------------------')

			sleep(5)