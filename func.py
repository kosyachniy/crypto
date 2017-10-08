import json, urllib, telebot, sqlite3, requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup

#Данные
currencies = []
with open('data/currencies.txt', 'r') as file:
	for i in file:
		currencies.append(json.loads(i[:-1]))

with open('data/exchangers.txt', 'r') as file:
	exchanges = json.loads(file.read())

#Telegram
with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())
	token = s['token']
	channelid = s['channelid']
	meid = s['meid']
	soid = s['soid']
bot = telebot.TeleBot(token)

'''
@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.send_message(message.chat.id, 'Hi!')

@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
	pass

@bot.message_handler(content_types=["text"])
def text(message):
	for i in range(len(x)):
		if x[i][0] == 1:
			x[i][0] = 0
			print(x[i][1:])
			bot.send_message(-1001124440739, 'BitCoin\n----------\nΔ +%f$\nT %d.%d %d:%d' % list(x[i][1:]))

	bot.send_message(message.chat.id, message.text)
	#delta, day, month, hour, minute
	print(message.chat.id, message.forward_from_chat)
'''

#if __name__ == '__main__':
#bot.polling(none_stop=True)

#SQLite
db=sqlite3.connect('data/main.db')

#Биржа
from functrade import *
stock = [YoBit()]