from pymongo import MongoClient

db = MongoClient()['crypto']
table = db['history']

for i in table.find():
	print(i)