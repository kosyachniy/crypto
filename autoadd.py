from func.data import db
from func.user import *
from time import sleep, strftime
import re, json

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())['read']
	tags = s['tags']
	from_id = s['channel']

messages = db['messages']

clean = lambda cont, words='': re.sub('[^a-zа-я' + words + ']', ' ', cont.lower()).split()
on = lambda x, y, words='': len(set(clean(x, words) if type(x) == str else x) & set(clean(y, words) if type(y) == str else y))

def replier(update):
	if isinstance(update, (UpdateNewMessage, UpdateNewChannelMessage)) and (update.message.from_id == from_id or update.message.to_id.channel_id == 1149594247): #from_id):
		print(update) #
		text = update.message.message

		try:
			text += '\n' + update.message.media.caption
		except:
			pass

		#+изображения

		#print(text)

		if on(text, tags, '#'):
			try:
				id = messages.find().sort('id', -1)[0]['id'] + 1
			except:
				id = 1

			print(id)

			doc = {'id': id, 'chat': update.message.from_id, 'message': update.message.id, 'text': text, 'time': strftime('%d.%m.%Y %H:%M:%S')}
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