from func.data import db
from func.user import *
from time import sleep
import re, json

with open('data/set.txt', 'r') as file:
	s = json.loads(file.read())['read']
	tags = s['tags']
	from_id = s['channel']

messages = db['messages']

get = lambda x=1: client.get_message_history(client.get_entity(from_id), x)[1]

clean = lambda cont, words='': re.sub('[^a-zа-я' + words + ']', ' ', cont.lower()).split()
on = lambda x, y, words='': len(set(clean(x, words) if type(x) == str else x) & set(clean(y, words) if type(y) == str else y))

def autoadd():
	num = get()[0].id
	print('!', num) #

	while True:
		last = get()[0].id
		for i in get(last - num):
			if i.id > num:
				#print(i)

				try:
					text = i.message
				except:
					text = ' '

				try:
					text += i.media.caption
				except:
					pass

				#+изображения

				#print(text)

				if on(text, tags, '#'):
					try:
						id = messages.find().sort('id', -1)[0]['id']
					except:
						id = 0

					print(id+1)

					doc = {'id': id+1, 'chat': from_id, 'message': num, 'text': text, 'time': strftime('%d.%m.%Y %H:%M:%S')}
					messages.insert(doc)

				num = i.id

		sleep(1)

if __name__ == '__main__':
	autoadd()