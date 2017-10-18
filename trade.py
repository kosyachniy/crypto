#Торговля по сигналам
from func import *

def trade():
#Определение последней необработанной операции
	#Начинает с после следующей исполненной операции
	num = 0
	try:
		with open('data/trade.txt', 'r') as file:
			for i in file:
				num = json.loads(i)['id']
	except:
		pass

	#num = 0

	while True:
#Подготовка операций к исполнению
		operation = []
		with open('data/trade.txt', 'r') as file: #Пока что операции не удаляются
			for i in file:
				cont = json.loads(i)
				if cont['id'] > num:
					operation.append(cont)
					num = cont['id']

		'''
		if len(operation):
			print('--!', operation)
		else:
			sleep(2)
			continue
		'''

		for i in operation:
#Рассчёт основных параметров для биржи
			#if i['exchanger'] == -1: i['exchanger'] = 1 #Биржа по умолчанию
			i['exchanger'] = 1 #Временная замена на одну биржу

			price = i['price'] if i['price'] else stock[i['exchanger']].price(i['currency'])
			if not price: continue #валюты нет или в малом объёме

			delta = stock[i['exchanger']].info() * i['volume']
			if delta < stock[i['exchanger']].min:
				delta = stock[i['exchanger']].min
			count = delta / price

			#сделать проверку достаточно ли средств

			time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
			rub = stock[i['exchanger']].ru()

#Покупка
			succ = stock[i['exchanger']].trade(i['currency'], count, price, 2)

			bot.forward_message(meid, i['chat'], i['mess'])
			bot.forward_message(soid, i['chat'], i['mess'])
			formated = 'Купить %s!\n-----\nК %.8f\nɃ %.8f (%d₽)\n∑ %.8f (%d₽)' % (currencies[i['currency']][1], count, price, price / rub, price * count, (price * count) / rub)
			bot.send_message(meid, formated)
			bot.send_message(soid, formated)

			if succ:
				'''
				#Ждать исполнения ордеров
				t = True
				for j in range(10):
					if stock[i['exchanger']].order(succ):
						t = False
						break
					sleep(5)

				if t:
					sett = [i['id'], succ, 0, 'buy', i['currency'], i['exchanger'], price, count, time, 0]
					print(sett)
					with open('data/history.txt', 'a') as file:
						print(json.dumps(sett), file=file)
					continue
				'''

				sett = [i['id'], succ, 0, 'buy', i['currency'], i['exchanger'], price, count, time, 0]
				print(sett)
				with open('data/history.txt', 'a') as file:
					print(json.dumps(sett), file=file)

				su = 0

				x = []
				for j in range(1, len(i['out'])+1):
					#Если слишком маленький объём продажи
					#может ли быть такое, что все кроме первого объединятся, а первый будет слишком маленький
					pric = i['out'][-j][2] if i['out'][-j][1] else price * i['out'][-j][2]
					coun = count * i['out'][-j][0]
					print('!!!COUN!!!', coun * pric)
					if coun * pric < stock[i['exchanger']].min:
						i['out'][-1-j][0] += i['out'][-j][0]
						continue

					su += coun * pric

					succ = 0 #stock[i['exchanger']].trade(i['currency'], coun, pric, 1)

					x.append([i['id'], succ, 0, 'sell', i['currency'], i['exchanger'], pric, coun, time])
				#Стоп-цена
				'''
				for j in range(len(x)-1):
					x[j].append(x[j+1][6])
				'''
				for j in range(len(x)-1):
					x[j].append(0)
				loss = i['loss'][1] if i['loss'][0] else i['loss'][1] * price
				x[len(x)-1].append(loss)
				
				with open('data/history.txt', 'a') as file:
					for j in range(1, len(x)+1):
						print(x[-j])
						print(json.dumps(x[-j]), file=file)

				#Худший - лучший случай
				vol = price * count
				loss = (price - i['loss'][1]) * count if i['loss'][0] else vol * (1 - i['loss'][1])
				formated = 'Худший случай: -%fɃ (-%d₽)\nЛучший случай: +%fɃ (+%d₽)' % (loss, loss / rub, su - vol, (su - vol) / rub)
				bot.send_message(meid, formated)
				bot.send_message(soid, formated) #
			else:
				print('Ошибка покупки!\n')
				bot.send_message(meid, 'Ошибка покупки!')
				#bot.send_message(soid, 'Ошибка покупки!') #
			bot.send_message(meid, '------------------------------')
			bot.send_message(soid, '------------------------------') #

if __name__ == '__main__':
	trade()