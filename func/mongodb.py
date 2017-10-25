#MongoDB
from pymongo import MongoClient
db = MongoClient()['crypto']
table = db['history']