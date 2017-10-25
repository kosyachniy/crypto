from func.main import *

currencies = []
with open('data/currencies.txt', 'r') as file:
	for i in file:
		currencies.append(json.loads(i[:-1]))

texted = lambda x: ''.join([i for i in x.lower() if i in 'qwertyuiopasdfghjklzxcvbnm.'])

exc = 0

@bot.message_handler(content_types=["text"])
def text(message):
	text = texted(message.text)
	start = gmtime().tm_min

	price = stock[exc].price(text) * 1.15
	volume = stock[exc].min / price #stock[exc].info() * 0.95
	order = stock[exc].trade(text, volume, price)

	t = False
	while not t:
		if stock[exc].order(order):
			t = True
		elif gmtime().tm_min - start >= 5:
			stock[exc].cancel(order)
			break

	if t:
		send('Успешно куплено!')
		order = stock[exc].trade(text, volume, price * 1.5, 'sell')

		while True:
			if stock.order(order):
				send('Успешно продано!')
				sleep(5)
	else:
		send('Ошибка покупки!')

if __name__ == '__main__':
	bot.polling(none_stop=True)