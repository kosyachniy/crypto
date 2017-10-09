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
1. Торговать на бирже
10. Определние ключевой информации: стопцена, объём
4. Алгоритм автоматического отслеживания ордеров
5. Только продажа без покупки
6. Временной промежуток между ордерами одной валюты
7. Добавить Bittrex
8. Контроль ордеров и стопцены
9. Что если в хештеге неизвестная валюта и он покупает другую?

Временные фиксы
---
1. Основная валюта - биткоины, всё выражается через неё, использование символики по умолчанию
