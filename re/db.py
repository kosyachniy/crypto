from pymongo import MongoClient

db = MongoClient()['crypto']

for i in db['messages'].find(): print(i)
for i in db['trade'].find(): print(i)
for i in db['history'].find(): print(i)