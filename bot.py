#Нельзя повторять одни и те же сигналы! - циклится
from func.main import *

try:
	num = messages.find_one({$query: {}, $orderby: {_id: -1}})['id']
except:
	num = 0

@bot.message_handler(content_types=["text"])
def text(message):
	print('!!!')
	try:
		chat, id, text = message.forward_from_chat.id, message.forward_from_message_id, message.text
	except:
		chat, id, text = message.chat.id, message.message_id, message.text

	if chat in admin:
		'''
#Команда
		if text in [*exchangers, 'PUMP', 'Информация']:
			smart(chat, text)
		'''
#Дальнейшая обработка
		num += 1
		doc = {'id': num, 'chat': chat, 'message': id, 'text': text}
		table.insert(doc)
	else:
		bot.send_message(chat, 'У вас нет доступа!')

'''
from info import info
from pump import pump

#Управление
def smart(chat, text):
	if text == 'Информация':
		info()
	elif text == 'PUMP':
		keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyb.add(types.KeyboardButton('Назад'))
		bot.register_next_step_handler(bot.send_message(chat, 'Введите криптовалюту', reply_markup=keyb), pumpit)
	else:
		keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyb.add(types.KeyboardButton('Сигнал', 'Покупка', 'Продажа', 'Назад'))
		bot.register_next_step_handler(bot.send_message(chat, exchangers.index(text), reply_markup=keyb), text) #не присоединяет биржу

def pumpit(message):
	if message.text == 'Назад':
		bot.send_message(chat, reply_markup=keyboard())
	else:
		pump(message.text)
'''

if __name__ == '__main__':
	bot.polling(none_stop=True)