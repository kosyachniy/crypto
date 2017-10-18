# КриптоАнализ

Источник | Ссылка
---|---
Канал Telegram | [@cryptosovet](https://t.me/cryptosovet)
Бот Telegram | [@CryptoSovetBot](https://t.me/CryptoSovetBot)

Биржи
---
Биржа | GitHub | API
---|---|---
YoBit | [NanoBjorn](https://github.com/NanoBjorn/yobit) | [yobit.net](https://yobit.net/ru/api/)
Bittrex | [EricSomdahl](https://github.com/ericsomdahl/python-bittrex) | [bittrex.com](https://bittrex.com/Home/Api)

Схема работы
---
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
5. Вывод чистой информации - балансы бирж
6. ??? Временной промежуток между ордерами одной валюты
7. Сделать очереди в мультипроцессинге чтобы библиотеки могли работать
8. Первая операция не записывается в history.txt

Временные фиксы
---
1. Основная валюта - биткоины, всё выражается через неё, использование символики по умолчанию
