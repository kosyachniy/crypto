from func.data import *
from func.trade import stock
from func.telegram import bot #

texted = lambda x: ''.join([i for i in x.lower() if i in 'qwertyuiopasdfghjklzxcvbnm.'])

exc = 0

'''
import telebot

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())
	token = s['token']
	channelid = s['channelid']
	meid = s['meid']
	soid = s['soid']
bot = telebot.TeleBot(token)
'''

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
		bot.send_message(meid, 'Успешно куплено!')
		order = stock[exc].trade(text, volume, price * 1.5, 'sell')

		while True:
			if stock.order(order):
				bot.send_message(meid, 'Успешно продано!')
				sleep(5)
	else:
		bot.send_message(meid, 'Ошибка покупки!')

if __name__ == '__main__':
	bot.polling(none_stop=True)