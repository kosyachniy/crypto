import json, urllib, telebot, requests #, sqlite3
from time import sleep, gmtime
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

#SQLite
#db=sqlite3.connect('data/main.db')

#Биржа
from functrade import *
stock = [YoBit(), Bittrex()]