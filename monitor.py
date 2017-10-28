#Контроль сигналов
from func.data import *
import math

#Данные
with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

on = lambda text, words: any([word in text for word in words])

alphabet = 'qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъёфывапролджэячсмитьбю'
clean = lambda cont, words: str(''.join([i if i in alphabet + words else ' ' for i in cont])).split()

def an(text, words, stop):
	cur = 0
	text = clean(text, words)
	for j in range(1, len(currencies)):
		if words + currencies[j][1].lower() in text or (words + currencies[j][0].lower() in text and currencies[j][0].lower() not in stop):
			print(j, currencies[j])
			if not cur:
				cur = j + 0
			else:
				return -1
	return cur

#БД
from pymongo import MongoClient
db = MongoClient()
messages = db['messages']
trades = db['trade']

def monitor():
#Первоначальные значения
	try:
		num = messages.find_one({'$orderby': {'_id': -1}})['id']
	except:
		num = 0

#Список новых сигналов
	while True:
		x = [i for i in messages.find({'$orderby': {'id': -1}})]

#Обработка
		for i in x:
			num = max(num, i['id'])
			#Убирать ссылки (чтобы не путать лишними словами), VIP
			text = i['text'].lower().replace(',', '.') #Сделать замену запятой на точку
			print(text)
			#time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

			loss = [0, 0.9] #
			out = []
			vol = 0
			price = 0

#Распознание сигнала
			#Условия необработки
			if on(text, vocabulary['stop']) or (len(clean(text, '')) * 1.5 > len(text) and len(text) > 70):
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
			for j in range(len(exchangers)):
				if exchangers[j][0].lower() in text:
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

			#Распознание размеров
			print('-!!-', on(text, vocabulary['loss'])) #
			print('!--!', text.count('\n')) #
			if ('\n' not in text) or (on(text, vocabulary['loss']) and text.count('\n') == 1):
				t = True
				text = text.split('\n')
				for j in text[0].split():
					try:
						if t:
							price = float(j)
							t = False
						else:
							if '%' in j:
								x = (1 - (int(re.findall(r'\d+', j)[0]) / 100)) * price
							else:
								x = float(j)
							out.append([0, 1, x])
					except:
						pass
				try:
					if '%' in text[1]:
						l = 1 - int(re.findall(r'\d+', text[1])[0]) / 100
						if l >= 0:
							loss = [0, l]
					elif '.' in text[1]:
						loss = [1, float(re.search(r'-?\d+\.\d*', text[1]).group(0))]
				except:
					pass
			else:
				for j in text.split('\n'):
					try:
						if on(j, vocabulary['buy']):
							price = float(re.search(r'-?\d+\.\d*', j).group(0))
							#Добавить разделение на несколько покупок
						elif on(j, vocabulary['sell']):
							out.append([0, 1, float(re.search(r'-?\d+\.\d*', j).group(0))])
					except:
						pass

				#Определение стоп-лосса
				for j in text.split('\n'):
					try:
						if on(j, vocabulary['loss']):
							if '%' in j:
								l = 1 - int(re.findall(r'\d+', j)[0]) / 100
								if l < 0:
									continue
								loss = [0, l]
							elif '.' in j:
								loss = [1, float(re.search(r'-?\d+\.\d*', j).group(0))]
					except:
						pass


			#Рассмотреть случай продажи валюты
			if cur >= 1 and buy != 1:
#Замены
				#Если не указаны объёмы покупки
				if not vol:
					vol = 0.03

				#Если не указаны ордеры на продажу
				if not len(out):
					out = [
						[0.5, 0, 1.1],
						[0.3, 0, 1.15],
						[0.1, 0, 1.2],
						[0.1, 0, 1.25]
					]

				#Если не указаны объёмы продажи
				if not out[0][0]:
					s = 0
					for j in range(len(out)):
						s += math.exp(j)
					x = 1 / s
					a = 0
					for j in range(len(out) - 1):
						out[-1 * (j + 1)][0] = math.exp(j) * x
						a += out[len(out) - j - 1][0]
					out[0][0] = 1 - a

#Отправка на обработку
				num += 1

				sett = {
					'id': i['id'],
					'currency': cur,
					'exchanger': exc,
					'price': price,
					'volume': vol,
					'out': out,
					'loss': loss,
					'term': term,
					'chat': i['chat'],
					'mess': i['message']
				} #, 'time': time

				#Если без покупки, первые поля пустые ?
				trades.insert(sett)

if __name__ == '__main__':
	monitor()