#Ведение канала
from func import *

#Данные
with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())
	channelid = s['channelid']
	meid = s['meid']

currencies = []
with open('data/currencies.txt', 'r') as file:
	for i in file:
		currencies.append(json.loads(i[:-1]))

with open('data/exchangers.txt', 'r') as file:
	exchanges = json.loads(file.read())

with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

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

on = lambda text, words: any([word in text for word in words])

alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъёфывапролджэячсмитьбю'
clean = lambda cont: str(''.join([i if i in alphabet else ' ' for i in cont])).split()

while True:
	with db:
		for i in db.execute("SELECT * FROM note WHERE act=1"):
			cur, exc, buy, count, operation, time, total, delta = i[2:]

			total = 0
			with db:
				for i in db.execute("SELECT * FROM currencies WHERE changer=(?) and currency=0", (exc,)):
					total = i[3]

			#убрать рассчёт доли при продаже
			print(total, cur, buy, exc)

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
			formated = '%s (%s)\n%s%s\n--------------------\n∑ %fɃ (%d₽)\nK %f\nΔ %s%fɃ (%s%d₽)' % (cur1, buys, exchanges[exc][0] + ' - ' if buy != 1 else '', cur2, total, total / rub, count, sign, delta, sign, delta / rub)

			#бота перенести в отдельный файл
			bot.send_message(meid, formated)
			bot.forward_message(meid, chat, id)

			t = [i[0] for i in exchanges]
			btc = [0] * len(exchanges)
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
			bot.send_message(meid, formated)
			bot.send_message(meid, '-----------------------------------')