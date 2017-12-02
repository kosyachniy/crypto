from pymongo import MongoClient

db = MongoClient()['crypto']
tables = ['messages', 'trade', 'history']

print('--------------------')
for j in tables:
	for i in db[j].find():
		print(i)
	print('--------------------')