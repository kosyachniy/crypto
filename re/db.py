from pymongo import MongoClient

db = MongoClient()['crypto']

print('--------------------')
for i in db['messages'].find(): print(i)
print('--------------------')
for i in db['trade'].find(): print(i)
print('--------------------')
for i in db['history'].find(): print(i)
print('--------------------')