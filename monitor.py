#Контроль сигналов
from func.data import *
import math

#Данные
with open('data/vocabulary.txt', 'r') as file:
	vocabulary = json.loads(file.read())

clean = lambda cont, words='': re.sub('[^a-zа-я' + words + ']', ' ', cont.lower()).split()
on = lambda x, y, words='': len(set(clean(x, words) if type(x) == str else x) & set(clean(y, words) if type(y) == str else y))
#on = lambda a, b: 1 if any([i in a for i in b]) else 0 #len(set(clean(a)) & set(b))

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

def stoploss(text, catch):
	try:
		if '%' in text:
			l = 1 - int(re.findall(r'\d+', text)[0]) / 100
			if l < 0: return catch
			return [0, l]
		elif '.' in text:
			return [1, float(re.search(r'-?\d+\.\d*', text).group(0))]
	except:
		return catch

def seller(text):
	if '%' in text:
		return [0, 0, 1 + int(re.findall(r'\d+', text)[0]) / 100]
	else:
		return [0, 1, float(re.search(r'-?\d+\.\d*', text).group(0))]

def recognize(i):
	#Убирать ссылки (чтобы не путать лишними словами), VIP
	text = i['text'].lower().replace(',', '.') #Сделать замену запятой на точку
	print(text)
	#time = strftime('%d.%m.%Y %H:%M:%S')

	loss = [0, 0.97] #
	reloss = loss + []
	out = []
	vol = 0
	price = 0

#Распознание сигнала
	#Условия необработки
	if on(text, vocabulary['stop'], '🚀$') or (len(clean(text)) * 1.5 > len(text) and len(text) > 70):
		return None

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
	if cur == -1: return None #если несколько валют

	print(cur, exc, term, buy)

	#Распознание размеров
	if ('\n' not in text) or (on(text, vocabulary['loss']) and text.count('\n') == 1):
		t = True
		text = text.split('\n')
		for j in clean(text[0], '.%0123456789'):
			try:
				if t:
					if '.' in j:
						price = float(j)
						t = False
				else:
					out.append(seller(j))
			except:
				pass
		if len(text) >= 2 and on(text[1], vocabulary['loss']):
			loss = stoploss(text[1], loss)
	else:
		for j in text.split('\n'):
			try:
				if on(j, vocabulary['buy']):
					price = float(re.search(r'-?\d+\.\d*', j).group(0))
					#Добавить разделение на несколько покупок
				elif on(j, vocabulary['sell']):
					out.append(seller(j))
			except:
				pass

		#Определение стоп-лосса
		for j in text.split('\n'):
			if on(j, vocabulary['loss']):
				loss = stoploss(j, loss)


	#Рассмотреть случай продажи валюты
	if cur >= 1 and buy != 1:
#Замены
		#Если не указаны объёмы покупки
		if not vol: vol = 0.05 #сделать фиксированные объёмы?

		#Если не указаны ордеры на продажу
		if not len(out):
			out = [
				[0.5, 0, 1.03],
				[0.3, 0, 1.05],
				[0.1, 0, 1.07],
				[0.1, 0, 1.1]
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

		#Если неправильно определил стоп-лосс
		if loss == None:
			loss = reloss

#Отправка на обработку
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
		return sett

def monitor():
#БД
	messages = db['messages']
	trades = db['trade']

#Первоначальные значения
	try:
		num = messages.find().sort('id', -1)[0]['id'] + 1
	except:
		num = 0

#Список новых сигналов
	while True:
		x = [i for i in messages.find({'id': {'$gt': num-1}})]

#Обработка
		for i in x:
			num = max(num, i['id'])

			x = recognize(i)
			if x:
				num += 1
				trades.insert(x)

if __name__ == '__main__':
	monitor()