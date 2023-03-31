<div>
    <img src="https://github.com/SultanovAsadbek/sultanovasadbek/blob/main/assets/to-do-list.gif" align="center"/>
</div>

## Описание
Это консольная программа поможет вам планировать задачи дня и эффективно управлять своим временем.

Что может делать программа:
- Добавление задачи в БД.
- Просмотр задачи.
- Удаление задачи.
- Изменение приоритет задачи.

Особенности программы:
- Анимированный индикатор выполнения.
- Автоматическое удаление вчерашних задач.
- Конкретное сообщение об ошибке.
- Зафиксирование все исключении в файл debug.log.
- Красочные тексты.
- Вывод задачи в виде таблицы для удобочитаемости. 
```
+----+---------------------+-----------+-----------------+------------------+ 
| id |       задача        | приоритет | дата добавления | время добавления |
+----+---------------------+-----------+-----------------+------------------+
| 2  | do python exercises |    8     |    31.10.2022    |     14:21:20     |
| 3  |       sleep         |    6     |    31.10.2022    |     14:23:00     |
+----+---------------------+-----------+-----------------+------------------+
```

## Язык программирование
![Python](https://img.shields.io/badge/python-black?style=for-the-badge&logo=python&logoColor=yellow)

## Библиотеки
![Rich](https://img.shields.io/badge/sqlite3-black?style=for-the-badge&logo=sqlite&logoColor=blue)
![Rich](https://img.shields.io/badge/rich-black?style=for-the-badge&logo=vector-logo-zone&logoColor=darkorange)
![Logur](https://img.shields.io/badge/loguru-black?style=for-the-badge&logo=vector-logo-zone&logoColor=darkslategray)
![Art](https://img.shields.io/badge/art-black?style=for-the-badge&logo=vector-logo-zone&logoColor=cadetblue)
![PrettyTable](https://img.shields.io/badge/prettytable-black?style=for-the-badge&logo=vector-logo-zone&logoColor=olive)

## База Данных
![Rich](https://img.shields.io/badge/sqlite-black?style=for-the-badge&logo=sqlite&logoColor=blue)

## Установка

1. Создать виртуальное окружение. 
<br> [Подробнее о виртуальном окружении](https://docs.python.org/3/library/venv.html)
```
python -m venv venv
```
2. Активировать виртуальное окрежение.
```
./venv/scripts/activate
```
3. Установка файл зависимостей.
```
pip install -r requirements.txt
```