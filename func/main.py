from func.data import *
from func.telegram import *
from func.trade import stock

#MongoDB
from pymongo import MongoClient
db = MongoClient()['crypto']
table = db['history']