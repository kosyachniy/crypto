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

ru = lambda: float(requests.get('https://blockchain.info/tobtc?currency=RUB&value=1000').text) / 1000

#Telegram
with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())
	token = s['token']
	channelid = s['channelid']
	meid = s['meid']
	soid = s['soid']
bot = telebot.TeleBot(token)

#SQLite
db=sqlite3.connect('data/main.db')

#Биржа