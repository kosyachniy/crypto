from func.data import db
from func.user import *
from time import sleep, strftime
import re, json

with open('data/set.txt', 'r', encoding='utf-8') as file:
	s = json.loads(file.read())['read']
	tags = s['tags']
	from_id = str(s['channel'])

messages = db['messages']

def tag(text): #! update.message.caption
	text = text.lower()
	for i in tags:
		if i in text:
			return True
	return False

def replier(update):
	if isinstance(update, (UpdateNewMessage, UpdateNewChannelMessage)) and str(update.message.to_id.channel_id) in from_id:
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