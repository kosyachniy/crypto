from pymongo import MongoClient

db = MongoClient()['crypto']
tables = ['messages', 'trade', 'history']

x = {}

for i in tables:
	x[i] = []
	for j in db[i].find():
		x[i].append(j)

#print(x)

import json
with open('db.json', 'w') as file:
	print(json.dumps(x), file=file)