# FlowerShop

Сайт цветочного магазина, позволяет оформить доставку праздничного букета. Имеется возможность подбора букета с помощью опроса клиента.

## Установка на локальном комопьютере

Для загрузки на локальный компьютер репозитория с проектом запустите в консоли команду
```
git clone https://github.com/YungIshimura/FlowerShop.git
```
или
```
git clone git@github.com:YungIshimura/FlowerShop.git
```

### Требования к окружению

Проект написан с использованием языка Python 3. 
Скачать и установить его можно по [ссылке](https://www.python.org/downloads/)
Необходимые для проекта библиотеки указаны в файле requirements.txt. Установить их можно с помощью команды:
```
pip3 install -r <путь до файла requirements.txt>
```
 #### Переменные окружения
 Переменные окружения должны быть описаны в файле .env, который должен лежать в корневой папке проекта.

 ```
 SECRET_KEY=<секретный ключ>
DEBUG=True
ALLOWED_HOSTS='127.0.0.1'
DB_URL=<url для используемой вами базы данных в формате dj-database-url>
 ```
 Форматы url баз данных можно посмотреть по [ссылке](https://pypi.org/project/dj-database-url/)

### Запуск проекта

Для локального запуска проекта используется команда 
```
python3 manage.py runserver
```

## Авторы
[Mark Tereshchenko](https://github.com/YungIshimura),
[Ilya Shirko](https://github.com/ilyashirko), [Aleksandr Popkov](https://github.com/popkovaleks)