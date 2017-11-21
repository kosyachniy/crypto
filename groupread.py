from func.user import *
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

from_id = -1001149594247 #-1001143136828
to_id = 136563129 #440219158

'''
l = PeerChannel(channel_id=from_id).stringify().format()
print(l)
'''
#print(dir(client))
print(client.get_entity(from_id))

for i in client.get_message_history(client.get_entity(from_id))[1]:
	'''
	print(i.id)
	print(i)
	'''

	y = '%d %d\n' % (from_id, i.id)

	try:
		x = i.message
	except:
		x = ''

	try:
		x += i.media.caption
	except:
		pass

	'''
	if not len(x):
		print('STOP')
		break
	'''

	client.send_message(to_id, y + x + '\n--------------------')