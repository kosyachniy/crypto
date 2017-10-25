#Нельзя повторять одни и те же сигналы! - циклится
from func.data import exchangers
from func.telegram import keyboard, bot
from info import info
from pump import pump

@bot.message_handler(content_types=["text"])
def text(message):
	print('!!!')
	try:
		chat, id, text = message.forward_from_chat.id, message.forward_from_message_id, message.text
	except:
		chat, id, text = message.chat.id, message.message_id, message.text

	if chat in admin:
#Команда
		if text in [*exchangers, 'PUMP', 'Информация']:
			smart(chat, text)
#Дальнейшая обработка
		with open('data/messages.txt', 'a') as file:
			print(json.dumps([chat, id, text], ensure_ascii=False), file=file)
	else:
		bot.send_message(chat, 'У вас нет доступа!')

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

if __name__ == '__main__':
	bot.polling(none_stop=True)