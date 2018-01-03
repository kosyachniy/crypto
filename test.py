from func.user import *
from telethon.tl.types import UpdateShortMessage, UpdateNewMessage, UpdateNewChannelMessage

def replier(update):
	if isinstance(update, (UpdateShortMessage, UpdateNewMessage, UpdateNewChannelMessage)): # and not update.out
		print(update.message.message)

client.add_update_handler(replier)
input('!')
client.disconnect()