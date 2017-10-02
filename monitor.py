#Контроль сигналов
from func import *

#Данные
with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

on = lambda text, words: any([word in text for word in words])

alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъёфывапролджэячсмитьбю'
clean = lambda cont: str(''.join([i if i in alphabet else ' ' for i in cont])).split()

'''
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
'''

ru = lambda: float(requests.get('https://blockchain.info/tobtc?currency=RUB&value=1000').text) / 1000

try:
	with open('data/trade.txt', 'r') as file:
		num = json.loads(file.read()[-1])['id']
except:
	num = 0

def monitor():
	@bot.message_handler(content_types=["text"])
	def text(message):
		'''
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
		'''
		i = [0, 0, message.text.lower()]
		print(i)
		#for i in x:
		exc = -1
		cur = -1
		#time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

		loss = [0, 0.9] #
		out = []
		vol = 0
		price = 0

#Распознание сигнала
		print(i[2])
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

		if on(i[2], vocabulary['short']):
			term = 0
		elif on(i[2], vocabulary['medium']):
			term = 1
		elif on(i[2], vocabulary['long']):
			term = 2
		else:
			term = -1

		t = 0
		text = clean(i[2])
		for j in range(1, len(currencies)):
			#print(text)
			if currencies[j][1].lower() in text or currencies[j][0].lower() in text:
				print(j, currencies[j])
				if t == 0:
					t = 1
				elif t == 1:
					t = 2
					break

				cur = j
		if t == 2: break #

		if cur >= 0:
#Замены
			if exc == -1: exc = 0 #Биржа по умолчанию
			exc = 0 #Временная замена на одну биржу

			if not len(out):
				out = [
					[0.5, 0, 1.1],
					[0.3, 0, 1.15],
					[0.1, 0, 1.2],
					[0.1, 0, 1.25]
				]

#Отправка на обработку
			num += 1

			sett = {
				'id': num,
				'currency': cur,
				'exchanger': exc,
				'price': price,
				'volume': vol,
				'out': out,
				'loss': loss,
				'term': term
			} #, 'time': time

			#Если без покупки, первые поля пустые
			with open('data/trade.txt', 'a') as file:
				print(json.dump(sett), file=file)
		
		sleep(5)

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
'''

if __name__ == '__main__':
	monitor()
	bot.polling(none_stop=True)