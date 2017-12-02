from pymongo import MongoClient

db = MongoClient()['crypto']
tables = ['messages', 'trade', 'history']

for i in tables:
	db[i].remove()