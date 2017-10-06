#Контроль сигналов
from func import *

#Данные
with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

on = lambda text, words: any([word in text for word in words])

alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъёфывапролджэячсмитьбю'
clean = lambda cont, words: str(''.join([i if i in alphabet + words else ' ' for i in cont])).split()

def an(text, words, stop):
	cur = 0
	text = clean(text, words)
	print(text)
	for j in range(1, len(currencies)):
		#print(text)
		if words + currencies[j][1].lower() in text or (words + currencies[j][0].lower() in text and currencies[j][0].lower() not in stop):
			print(j, currencies[j])
			if not cur:
				cur = j + 0
			else:
				return -1
	return cur

def monitor():
#Первоначальные значения
	chat, id = 0, 0
	try:
		with open('data/messages.txt', 'r') as file:
			for i in file:
				chat, id, _ = json.loads(i)
	except:
		pass

	#chat, id = 0, 0

	num = 0
	try:
		with open('data/trade.txt', 'r') as file:
			for i in file:
				num = json.loads(i)['id']
	except:
		pass

	#print('--', num)

#Список новых сигналов
	while True:
		t = False if chat !=0 and id != 0 else True
		x = []
		with open('data/messages.txt', 'r') as file:
			for i in file:
				y = json.loads(i)
				if t:
					x.append(y)
					chat, id, _ = y
				elif y[0] == chat and y[1] == id:
					t = True

		sleep(2)
		#print(len(x))

#Обработка
		for i in x:
			#Убирать ссылки (чтобы не путать лишними словами), VIP
			text = i[2].lower()
			print(text)
			#time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

			loss = [0, 0.9] #
			out = []
			vol = 0
			price = 0

#Распознание сигнала
			#Условия необработки
			if on(text, vocabulary['stop']) or (len(clean(text, '')) * 1.5 > len(text) and len(text) > 70):
				bot.send_message(meid, 'stop: %s\nlen:%b' % (str(on(text, vocabulary['stop'])), len(clean(text, '')) * 1.5 > len(text) and len(text) >70))
				continue

			#Определение сигнал покупки / продажи
			if on(text, vocabulary['buy']):
				buy = 2
			elif on(text, vocabulary['sell']):
				buy = 1
			else:
				buy = 0

			#Определение биржи
			exc = -1
			for j in range(len(exchanges)):
				if exchanges[j][0].lower() in text:
					exc = j
					break

			#Определение срока
			if on(text, vocabulary['short']):
				term = 0
			elif on(text, vocabulary['medium']):
				term = 1
			elif on(text, vocabulary['long']):
				term = 2
			else:
				term = -1

			#Определение валюты
			cur = an(text, '#', ['status']) #поиск по хештегу
			if cur <= 0: cur = an(text, '', ['status']) #сделать список стоп слов, которые не учитываются в поиске валют
			if cur == -1: continue #если несколько валют

			print(cur, exc, term, buy)

			'''
			#Распознание размеров
			for j in text.split('\n'):
				parse = j.split(' ')
				if on(j, vocabulary['buy']):
					for u in parse:
						try:
							float(u)
					buys.append()
			'''

			#Рассмотреть случай продажи валюты
			if cur >= 1 and buy != 1:
#Замены
				if not vol:
					vol = 0.03

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
					'term': term,
					'chat': i[0],
					'mess': i[1]
				} #, 'time': time

				#Если без покупки, первые поля пустые ?
				with open('data/trade.txt', 'a') as file:
					print(json.dumps(sett), file=file)

if __name__ == '__main__':
	monitor()