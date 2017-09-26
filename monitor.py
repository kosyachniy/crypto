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
	'buy': {'buy', 'купить', 'покупаем', 'докупаем', 'докупаемся'},
	'sell': {'sell', 'продать', 'продаём', 'продаем'}
}

url='https://ru.investing.com/crypto/currencies'
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
		price = td[3].text.replace('.', '')
		
		if index.lower() == x:
			print(name, index, price)
			return price

on = lambda text, words: any([word in text for word in words])

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
		rub = price('BTC')

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
		for j in range(len(currencies)):
			if currencies[j][1].lower() in i[2] or currencies[j][0].lower() in i[2]:
				if t == 0:
					t = 1
				elif t == 1:
					t = 2
					break

				cur = j
		if t == 2: continue #

		total = 0
		with db:
			for i in db.execute("SELECT * FROM currencies WHERE changer=(?) and currency=-1", (exc,)):
				total = i[3]

		#убрать рассчёт доли при продаже

#Определение количества
		operation = price(currencies[cur][1])
		delta = total * 0.03
		count = delta / operation

		#постваить процент, после которого сделка совершится
		if buy or cur>=0:
			print(cur) #
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

			#T %d.%d %d:%d , day, month, hour, minute
			formated = '%s (%s)\n%s%s\n--------------------\n∑ %f%s (%d₽)\nK %f\nΔ %s%f%s (%s%d₽)' % (cur1, buy, exchanges[exc][0] + ' - ' if exc else '', cur2, total, transfer, total / rub, count, sign, delta, transfer, sign, delta / rub)

			#бота перенести в отдельный файл
			bot.send_message(meid, formated)
			bot.forward_message(meid, chat, id + 2)
			bot.send_message(meid, 'Сводка\n--------------------\nYObit\n\n--------------------\nBittrex\n\n--------------------\nPoloniex\n')
			bot.send_message(meid, '----------------------------------------')
			#запись в базу данных

			sleep(5)