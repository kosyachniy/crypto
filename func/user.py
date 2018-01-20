from telethon import TelegramClient
from telethon.tl.types import UpdateShortMessage, UpdateNewMessage, UpdateNewChannelMessage #PeerChannel #PeerUser, PeerChat

import json
with open('data/keys.txt', 'r', encoding='utf-8') as file:
	x = json.loads(file.read())['telegram']['user']

client = TelegramClient('data/'+x['name'], x['id'], x['hash'], update_workers=4)
client.connect()

if not client.is_user_authorized():
	client.send_code_request(x['phone'])
	client.sign_in(x['phone'], input('Код: '))