from func import *

currencies = []
with open('data/currencies.txt', 'r') as file:
	for i in file:
		currencies.append(json.loads(i[:-1]))

texted = lambda x: ''.join([i for i in x.lower() if i in 'qwertyuiopasdfghjklzxcvbnm.'])

@bot.message_handler(content_types=["text"])
def text(message):
	text = texted(message.text)
	start = gmtime().tm_min

	price = stock[1].price(text) * 1.15
	volume = stock[1].min / price #stock[1].info() * 0.95
	order = stock[1].trade(text, volume, price)

	t = False
	while not t:
		if stock[1].order(order):
			t = True
		elif gmtime().tm_min - start >= 5:
			stock[1].cancel(order)
			break

	if t:
		send('Успешно куплено!')
		order = stock[1].trade(text, volume, price * 1.5, 'sell')

		while True:
			if stock.order(order):
				send('Успешно продано!')
				sleep(5)
	else:
		send('Ошибка покупки!')

if __name__ == '__main__':
	bot.polling(none_stop=True)