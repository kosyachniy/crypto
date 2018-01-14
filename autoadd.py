from func.data import db
from func.user import *
from time import sleep, strftime
import re, json

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())['read']
	tags = s['tags']
	from_id = s['channel']
	channel_id = s['id']

messages = db['messages']

def tag(text):
	for i in tags:
		if i in text:
			return True
	return False

def replier(update):
	if isinstance(update, (UpdateNewMessage, UpdateNewChannelMessage)) and (update.message.from_id == from_id or update.message.to_id.channel_id == channel_id): #from_id):
		#print(update)
		text = update.message.message

		try:
			text += '\n' + update.message.media.caption
		except:
			pass

		#+изображения

		if tag(text):
			try:
				id = messages.find().sort('id', -1)[0]['id'] + 1
			except:
				id = 1

			doc = {
				'id': id,
				'chat': update.message.from_id,
				'message': update.message.id,
				'text': text,
				'time': strftime('%d.%m.%Y %H:%M:%S')
			}
			messages.insert(doc)

client.add_update_handler(replier)
input('!')
client.disconnect()
print('!!')
'''
while True:
	try:
		client.add_update_handler(replier)
		input()
	except:
		pass
'''