# Анализ биржи криптовалюты (CryptoAnalysis)

Источник | Ссылка
---|---
Канал Telegram | [@cryptosovet](https://t.me/cryptosovet)
Бот Telegram | [@CryptoSovetBot](https://t.me/CryptoSovetBot)

Биржи
---
№ | Биржа | GitHub | API
---|---|---
0 | [YoBit](https://yobit.net/ru/wallets/) | [NanoBjorn](https://github.com/NanoBjorn/yobit) | [yobit.net](https://yobit.net/ru/api/)
1 | [Bittrex](https://bittrex.com/Balance) | [EricSomdahl](https://github.com/ericsomdahl/python-bittrex) | [bittrex.com](https://bittrex.com/Home/Api)

Схема работы
---
Операция | Mac | Linux | Windows
---|---|---|---
Подготовка | ```  ``` | ``` wget https://bootstrap.pypa.io/get-pip.py<br>sudo python3 get-pip.py<br>pip install vk_api bs4 matplotlib pymongo<br>sudo apt-get install python3-tk python-tk -y<br>pip install PyTelegramBotAPI==2.2.3<br>lsof -i:27017<br>sudo apt-get install mongodb<br>sudo service mongodb start<br>tail -n200 /var/log/mongodb/mongodb.log<br>git clone https://github.com/kosyachniy/crypto<br>...<br>...<br>tmux<br>cd crypto ``` | ```  ```
Запуск | ``` mongod<br>./main ``` | ``` ./main ``` | ```  ```

Получение сигналов | Обработка | Исполнение
---|---|---
``` autoadd.py ``` | ``` monitor.py ``` | ``` bot.py ```
``` main.py ``` |  | ``` trade.py ```
``` ``` |  | ``` autotrade.py ```

Сделать
---
1. Странное поведение при указании покупки как 0.0<br>Сделать в таком случае автоматическое определение действующей цены
2. Определние объёма
3. Проверить процентное и статические значения распознания ботом ключевой информации
4. Только продажа без покупки
5. Оформить бота с кнопками и ключевыми командами для удобного управления
6. ??? Временной промежуток между ордерами одной валюты
7. Сделать очереди в мультипроцессинге чтобы библиотеки могли работать
8. ??? Первая операция не записывается в MongoDB
9. Понижать ордеры на долгосроках
10. Запуск из одного файла - multiprocessing
11. Синхронизация и бэкап данных
12. Пампы
13. ICO

Временные фиксы
---
1. Основная валюта - биткоины, всё выражается через неё, использование символики по умолчанию
2. Не распознаёт сигналы с несколькими валютами
3. Не разделяет сигналы с несколькими покупками
4. Стоит замена указываемой цены в сигнале на действующую
