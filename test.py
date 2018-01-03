from func.user import *
from telethon.tl.types import UpdateShortMessage, UpdateNewMessage, UpdateNewChannelMessage

def replier(update):
	print(update)
	if isinstance(update, (UpdateShortMessage, UpdateNewMessage, UpdateNewChannelMessage)): # and not update.out
		if isinstance(update, UpdateShortMessage):
			print(update.message)
		else:
			print(update.message.message)
			print(update.message.to_id.channel_id)

		try:
			print(update.message.media.caption)
		except:
			pass

client.add_update_handler(replier)
input('!')
client.disconnect()