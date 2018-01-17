# Анализ биржи криптовалюты (CryptoAnalysis)

Источник | Ссылка
---|---
Канал Telegram | [@cryptosovet](https://t.me/cryptosovet)
Бот Telegram | [@CryptoSovetBot](https://t.me/CryptoSovetBot)

![Запуск бота](2.png)

Биржи
---
№ | Биржа | GitHub | API
---|---|---|---
0 | [YoBit](https://yobit.net/ru/wallets/) | [NanoBjorn](https://github.com/NanoBjorn/yobit) | [yobit.net](https://yobit.net/ru/api/)
1 | [Bittrex](https://bittrex.com/Balance) | [EricSomdahl](https://github.com/ericsomdahl/python-bittrex) | [bittrex.com](https://bittrex.com/Home/Api)
2 | [Poloniex](https://poloniex.com/) | [s4w3d0ff](https://github.com/s4w3d0ff/python-poloniex) | [poloniex.com](https://poloniex.com/support/api/)

Схема работы
---
``` pip install -r requirements.txt ```

Операция | Mac | Linux | Windows
---|---|---|---
Настройка | ```  ``` | ``` wget https://bootstrap.pypa.io/get-pip.py ``` <br> ``` sudo python3 get-pip.py ``` <br> ``` pip install vk_api bs4 matplotlib pymongo ``` <br> ``` sudo apt-get install python3-tk python-tk -y ``` <br> ``` pip install PyTelegramBotAPI==2.2.3 ``` <br> ``` lsof -i:27017 ``` <br> ``` sudo apt-get install mongodb ``` <br> ``` sudo service mongodb start ``` <br> ``` tail -n200 /var/log/mongodb/mongodb.log ``` <br> ``` git clone https://github.com/kosyachniy/crypto ``` <br> ``` ... ``` <br> ``` ... ``` <br> ``` tmux ``` <br> ``` cd crypto ``` | ```  ```
Запуск | ``` mongod ``` <br> ``` ./main ``` | ``` ./main ``` | ```  ```

![Порядок запуска](1.png)

Отсутствующие файлы
---
Номер | Имя | Цель
---|---|---
1 | ``` data/keys.txt ``` | Ключи
2 | ``` data/*.session ``` | Сессии пользователей Telegram
3 | ``` re/db/mongo ``` | База данных (необязательна)

Сделать
---
1. Определние объёма
4. Только продажа без покупки
6. ??? Временной промежуток между ордерами одной валюты
7. Сделать очереди в мультипроцессинге чтобы библиотеки могли работать
9. Понижать ордеры на долгосроках
10. Запуск из одного файла - multiprocessing
11. Синхронизация и бэкап данных
13. ICO
14. ??? Не покупать, если слишком маленький объём и это не памп
16. Возвращать с бирж количество сколько купили валюты
18. На пампах сделать кнопку выхода
19. ??? Перенести продажу в модуль автотрейдинга
23. Автоматическое определние курса продажи в пампах (закрытие первой волны)
24. Экстренная продажа и закрытие ордеров и продажа по сигналам
27. Сделать в боте проверку курсов валют и получение графиков
28. Несколько раз присылает информацию с бирж в временной промежуток
29. Ошибка при чтении из бота на долгом времени
31. При ценовом диапозоне выбирать наибольшую цену
34. Добавление новых валют
35. Проверить дробные проенты в сигналах
36. Временное ограничение для сигналов 5, 13, 18 часов минус 1% ордера +1% стоп-лосс
39. Автоматическая докупка маленькой валюты, чтобы продать
41. ??? Если уже был 5% рост - не покупать
44. Ошибка с распознанием сигнала от #PrivateSignals
45. Отменять покупку по дельте курса с момента подачи заявки
46. Распознание сатошей
47. При ручном закрытии отмечает ордер успешно выполненым
50. Так как на биржу YoBit отправляется nonce по времени, очень быстрые операции не проходят
51. Шаблоны сообщений в файлы настроек
53. Почему не принимает сигналы VIP_INSIDE
54. Бот пишет что вышло время на тех заказах, которых уже нет
55. Валюта May, Dollar
57. На графики подписи у цели, водяные знаки наших каналов, название валюты
58. Покупка ltc, eth, bcc при падении битка 30% 30% 40% +5 +7 +10
59. Если падает биток, покупать продаваться в доллар выход: +3 -3 рост час
60. trade разбить на monitor и stock, в monitor вынести замены из recognize
61. График сам масштабируется, если на минутной временной ленте мало изменений / изменить масштаб
62. Объединять все стоп-лоссы валюты в один (так как пониженная сумма и могут не пройти)
63. Почему при выставление ордеров продажи, остаётся на балансе маленький остаток
64. Не работают стоп-лоссы на всех ордерах одного сообщения
65. Просчитывать минимальные суммы для конкретных валют
66. Получает ли бот старые сообщения при запуске?
67. Добавить обработку медиа
68. Время в timestamp
69. Что быстрее мой метод получения сообщений или Telethon Update? Можно ли ускорить?
70. Проверка, что сообщение недавнее
71. Долго получает YoBit
72. Перенести исключения в глубину к price
73. Проверить время работы разных функций и время запии в разные ДБ
74. Переписать некоторые модули на C++
75. Случаи с несколькими покупками
76. Случай с однострочным сообщением с stop-loss
77. Случай с несколькими валютами в одном сигнале
78. Случай с покупкой относительно usd, eth, ltc и тд
79. Случай с несколькими покупками в одном сигнале относительно разных валют

Временные фиксы
---
1. Основная валюта - биткоины, всё выражается через неё, использование символики по умолчанию
2. Не распознаёт сигналы с несколькими валютами
3. Не разделяет сигналы с несколькими покупками
4. Покупает по цене на бирже, а не установленной в сигнале
5. Первый день в канале - прописанные в коде суммы

Модули
---
Управление ботом
1. Кнопки
2. Пампы
3. Информация
4. Настройки
5. Сигналы
вход: Telegram сообщения
выход: файл с сообщениями / запуск под функций

Обработка сигналов
1. Однострочные, двухструнные мои
2. Многострочные мои
3. Выделение построчное
4. Замена на стандартную информацию
вход: файл с сообщениями
выход: выделенная информация в БД

Ведение канала
1. Форматирование информации
вход: выделенная информация в БД
выход: канал Telegram

Определение параметров для бирж
1. Рассчёт основных параметров для соответствующей биржи
вход: выделенная информация в БД
выход: операции на бирже в БД

v перенести покупку сюда v

Биржа
1. Выставление покупки
2. Стоп-лоссы
3. Контроль исполнения
4. Выставление продажи
вход: операции на бирже в БД
выход: ордеры на биржах

Пампы
1. Быстрое выставление нужных параметров
вход: валюта и биржа
выход: ордеры на биржах

x убрать этот модуль в функционал x

Информация
1. Вывод основной информации
выход: сообщения Telegram
