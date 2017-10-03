from func import *

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

def bot():
	#сделать контроль последнего обработанного id

	num = 0
	with open('data/trade.txt', 'r') as file:
		try:
			for i in file:
				num = json.loads(i)['id']
		except:
			pass

	print(num)
	num = 0 #

	while True:
		operation = []
		with open('data/trade.txt', 'r') as file:
			for i in file:
				x = json.loads(i)
				if x['id'] > num:
					operation.append(x)

		rub = 250000 #rub = ru()
		for i in operation:
			formated = '%s\n'  % (currencies[i['currency']][1],)
			if i['exchanger'] != -1:
				formated += exchanges[i['exchanger']][0] + ' - '
			formated += currencies[i['currency']][0]
			if i['term'] == 0:
				formated += ' - краткосрочный'
			elif i['term'] == 1:
				formated += ' - среднесрочный'
			elif i['term'] == 2:
				formated += ' - долгорочный'
			'''
			formated += '\nX %.8fɃ (%d₽)' % (i['price'], i['price'] / rub)
			if total != -1:
				formated += '\n--------------------\n∑ %fɃ (%d₽)\nK %f\nΔ %s%fɃ (%s%d₽)' % (total, total / rub, count, sign, delta, sign, delta / rub)
			formated += '\n--------------------\n∑ %fɃ (%d₽)\nK %f\nΔ %s%fɃ (%s%d₽)' % (total, total / rub, count, sign, delta, sign, delta / rub)
			'''
			formated += 'Покупка:\nɃ %f\nK %d%%\n↓ %s\n' % (i['price'], i['volume'] * 100, str(i['loss'][1]) + 'Ƀ' if i['loss'][0] else str(int(i['loss'][1] * 100)) + '%')
			for j in i['out']:
				formated += '\nV %d%% - %s' % (j[0] * 100, str(j[2]) + 'Ƀ' if j[1] else '+' + str(round((j[2] - 1) * 100)) + '%')

			#print(formated)
			bot.send_message(sendid, formated)

if __name__ == '__main__':
	bot()

'''
		if cur >= 1:
#Определение основной информации
			#ели указана биржа - входить в неё
			if exc != -1: exc = 0 #временная замена биржи на используемую
			#for по вем биржам - первая, которая сработает
			operation = stock[0].price(cur, buy)

			if operation: #также решается проблема, если биржа пришлёт нулевое значение
				total = stock[0].info() #разобраться в синхронизации БД и биржи
				'\''
				for j in db.execute("SELECT * FROM currencies WHERE currency=0 and changer=(?)", (exc,)):
					total = j[3]
				'\''
				new = 0

				if buy != 1:
					delta = total * 0.03
					count = delta / operation
					delta *= 1 + stock[0].comm
					new = total - delta

					succ = stock[0].trade(cur, count, operation, buy)

					t = True
					for j in db.execute("SELECT * FROM currencies WHERE currency=(?) and changer=(?)", (cur, exc)):
						t = False
						db.execute("UPDATE currencies SET count=(?), price=(?) WHERE currency=(?) and changer=(?)", (j[]))

					db.execute("INSERT INTO currencies (currency, changer, count, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (cur, exc, count, operation, time, *succ))
				else:
					count = 0 #количество этой валюты на бирже
					delta = count * operation * (1 - stock[0].comm)
					new = total + delta

					succ = stock[0].trade(cur, count, operation, buy)

					'\''
					if succ:
						#удалить из БД
					else:
						#добавить минусовое поле #
					'\''

				if succ[0]:
					db.execute("UPDATE currencies SET count=(?) WHERE currency=0 and changer=(?)", (new, exc))

#Торговля
				#+ контроль ошибок + контроль есть что продавать + контроль есть ли смысл покупать (малые размеры)
#Сборка сообщения на Telegram-канал
				#bot.send_message(sendid, 'YoBit - %s: %.10f - %.10f' % (currencies[cur][1], ))
			else:
				exc = -1
				total = -1
				operation = price(currencies[cur][1])
				delta = -1
				count = -1
				#db.execute("UPDATE operations SET time2=0 WHERE id=(?)", (i[0],))
			#db.execute("INSERT INTO operations (act, currency, changer, buy, per, meschat, mesid, time1) VALUES (1, ?, ?, ?, 0.03, ?, ?, ?)", (cur, exc, buy, chat, id, time))
			#Добавление в БД с обменщиком -1, игра на несущетвующей бирже

			sign = '±+-'[buy]
			buys = ['не определено', 'продать', 'купить'][buy]

			if cur == -1:
				cur1 = 'Криптовалюта не определена'
				cur2 = 'Индекс не определён'
			else:
				cur1 = currencies[cur][0]
				cur2 = currencies[cur][1]

			rub = ru()

			formated = '%s (%s)\n'  % (cur1, buys)
			if buy != 1 and exc != -1:
				formated += exchanges[exc][0] + ' - '
			formated += cur2
			if len(term):
				formated += ' - ' + term
			formated += '\nX %.8fɃ (%d₽)' % (operation, operation / rub)
			if total != -1:
				formated += '\n--------------------\n∑ %fɃ (%d₽)\nK %f\nΔ %s%fɃ (%s%d₽)' % (total, total / rub, count, sign, delta, sign, delta / rub)

			#бота перенести в отдельный файл
			bot.send_message(sendid, formated)
			bot.forward_message(sendid, chat, id)

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

		sleep(5)
'''