import json, requests, re
from time import sleep, gmtime, strftime, strptime, mktime

#Данные
with open('data/currencies.txt', 'r', encoding='utf-8') as file:
	currencies = [json.loads(i) for i in file]

with open('data/exchangers.txt', 'r', encoding='utf-8') as file:
	exchangers = json.loads(file.read())

with open('data/set.txt', 'r', encoding='utf-8') as file:
	s = json.loads(file.read())
	utc = s['utc']
	excd = s['replacements']['exchanger']

#MongoDB
from pymongo import MongoClient
db = MongoClient()['crypto']