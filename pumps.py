import telebot, json
from functrade import Bittrex
from time import gmtime

currencies = []
with open('data/currencies.txt', 'r') as file:
	for i in file:
		currencies.append(json.loads(i[:-1]))

texted = lambda x: ''.join([i for i in x.lower() if i in 'qwertyuiopasdfghjklzxcvbnm.'])

stock = Bittrex()

@bot.message_handler(content_types=["text"])
def text(message):
	text = texted(message.text)
	start = gmtime().tm_min

	price = stock.price(text) * 1.15
	volume = stock.info() * 0.95 / price
	order = stock.trade(text, volume, price)

	t = False
	while not t:
		if stock.order(order):
			t = True
		elif gmtime().tm_min - start >= 5:
			break

	if t:
		bot.send_message(meid, 'Успешно куплено!')
		#bot.send_message(soid, 'Успешно куплено!')

		order = stock.trade(text, volume, price * 1.5, 'sell')
	else:
		bot.send_message(meid, 'Ошибка покупки!')
		#bot.send_message(soid, 'Ошибка покупки!')

	while True:
		if stock.order(order):
			bot.send_message(meid, 'Успешно продано!')
			#bot.send_message(soid, 'Успешно продано!')

if __name__ == '__main__':
	bot.polling(none_stop=True)