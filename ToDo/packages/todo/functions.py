import sqlite3
import time
from loguru import logger
from prettytable import PrettyTable
from packages.todo.beatiful import success
from packages.todo.exceptions import NameExc
from packages.todo.exceptions import PriorityExc
from packages.todo.exceptions import IdExc
from packages.todo.exceptions import TypeExc


class ToDo:
    """Класс описывает Список задачи.

    Аттрибуты:
    --------------
    |--Все аттрибуты экземпляра являются приватными.--|
    | t_priority : int
        приоритет задачи.
    | f_t_name : str
        имя задачи
    | connection : sqlite3.Connection
         аттрибут отвечает за соединение к файлу с расширением (.db База данных)
    | cur : sqlite3.Cursor
        аттрибут отвечает за сохранение изменение в файле с расширением (.db База данных)


    Методы:
    -----------
    | add_task(self)
        добавление данных в файл с расширением (.db база данных)
    | show_task(self)
        просмотр данных из файла с расширением (.db база данных)
    | update_priority(self)
        изменение и обновление номер приоритета задачи
    |delete_task(self)
        удаление данные в файле с расширением (.db база данных)
    |close_connection(self)
        закрытие файла с расширением (.db база данных)

    Приватные методы:
    -----------------
    | create_table(self)
        создать таблицу в файле с расширением (.db база данных)
        метод сработает при создании экземпляр класса
    | count_tasks(self)
        проверка количество задачи из файла с расширением (.db база данных)
        метод вызывается в методе [--add_task()--]
    | find_task(self)
        поиск задачи по сходимости
        метод вызывается в методе [--add_task()--]
    | automate_delete(self)
        метод автоматически удаляет старые задачи
        для освобождения мест в таблице из файла с расширением (.db база данных)
    """

    def __init__(self):
        """
        Параметры:
        -----------
        отсутствует

        """
        logger.remove()
        logger.add(
            "debug.log",
            format="{time} {level} {message}",
            rotation="10 MB",
            compression="zip",
        )

        self.__connection = sqlite3.connect("todo.db")
        self.__cur = self.__connection.cursor()

        self.__create_table()
        self.__automat_delete_task()

    def __create_table(
        self: sqlite3.SQLITE_CREATE_TABLE,
    ) -> sqlite3.SQLITE_CREATE_TABLE:
        """
        * Метод создаёт таблицу в файле todo.db (База данных)
        * Метод автоматически вызывается в конструкторе [ __init__(self) ].

        Параметры:
        ----------
        отсутствует

        """

        #  sql запрос на создание таблицы в файле todo.db
        #  создать таблицу если таблица не создана.
        self.__cur.execute(
            """CREATE TABLE IF NOT EXISTS tasks(
            id_task INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            priority INTEGER NOT NULL,
            date TEXT NOT NULL,
            time_task TEXT NOT NULL
        )"""
        )

    def add_task(self: sqlite3.SQLITE_INSERT) -> sqlite3.SQLITE_INSERT:
        """
        * Метод отвечает за добавление задачи в файл todo.db (База данных)
        * Метод вызывается по необходимости/желанию пользователя.

        Параметры:
        -----------
        отсутствует

        """

        # Проверка на количество задачи в базе данных.
        # Если количество задачи 15, метод предупреждает и прерывает программу.
        self.__count_tasks()

        # Если строка пустая или строка состоит только из пробелов ...
        self.__t_name = input("Задача: ").lower().strip()

        if len(self.__t_name) == 0 or self.__t_name.isspace():
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл пустую строку или не корректные данные.\n \
                        Введённая значения: [{self.__t_name}]"
            )
            # вызвать исключение с сообщением и прервать программу.
            raise NameExc(message="Введённые данные не корректны!")

        if len(self.__t_name) <= 7:
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл не корректные данные.\n \
                        Введённая значения: [{self.__t_name}]\n \
                        Количество значений в введённой строке: [{len(self.__t_name)}]\n \
                        Минимальная ожидаемое количество значений в строке: 7"
            )
            raise NameExc(
                message=f"\nУказанная количества значений: {len(self.__t_name)}"
                f"\nМинимальная количества значений: 7"
            )
            
        # Проверка на уникальность задачи.
        # Если задача существует в файле todo.db (База данных), метод предупреждает и прерывает программу.
        self.__find_task()

        self.__t_priority = input("Приоритет: ").lower().strip()

        # Проверка введённых значений на типы данных.
        # Если тип данных значения 'str' или не указана значения...
        if self.__t_priority.isalpha() == True or len(self.__t_priority) == 0:
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл 'str' вместо 'int'.\n \
                        Введённая значения: [{self.__t_priority}] --> 'str'\n \
                        Ожидаемая значения: [1, 2, 3, 4, ...] --> 'int'"
            )

            # вызвать исключение и прервать программу.
            raise TypeExc(message="'Приоритет' принимает только числовое значение!")

        # Проверка приоритет задачи.
        # Если приоритет вне диапазона [1:10] ...
        if int(self.__t_priority) not in range(1, 11):
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл число вне диапозона. [1:10]\n \
                        Введённая значения: [{self.__t_priority}] >= [1:10]\n \
                        Ожидаемая значения: [{self.__t_priority}] <= [1:10] "
            )
            # предупреждать и прерывать программу.
            raise PriorityExc(message="Приоритет указан вне диапазона [1: 10]!")

        # [1] Группировать данных в список.
        values = [
            self.__t_name,
            self.__t_priority,
            time.strftime("%d.%m.%Y"),
            time.strftime("%H:%M:%S"),
        ]

        # [2] Преобразовать в кортеж, так как файл todo.db принимает кортеж для записи данных.
        # [3] Запись в файл todo.db (База данных).
        self.__cur.execute(
            """INSERT INTO tasks (name, priority, date, time_task) VALUES(?, ?, ?, ?)""",
            tuple(values),
        )
        self.__connection.commit()

    def __count_tasks(self: sqlite3.SQLITE_SELECT) -> sqlite3.SQLITE_SELECT:
        """
        * Метод считает количество задачи из файла todo.db (База данных).
        * Если количество задачи больше 15, метод вызывает исключение.
        * Метод вызывается автоматически в методе [-- add_task(self) --].

        Параметры:
        ----------
        отсутствует

        """

        try:
            # [1] Получит общее количество задачи.
            last_id = self.__cur.execute("SELECT COUNT(*) FROM tasks").fetchone()
            # [2] Если количество задача больше 15...
            if last_id[0] > 15:
                # Регистрировать ошибку в файл 'debug.log'.
                logger.error(
                    f"Описание: Максимальное вместимость в таблице 15 задач\n пользователь пытался записать 16-ое заачи."
                )
                # [2.1] вызвать исключение с сообщением и прервать программу.
                raise IdExc(message="Количество задачи больше 15!")

        except (sqlite3.DatabaseError, IndexError) as error:
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Утечка в базе данных(sqlite3) или в индексации.\n \
                        Ошибка: [{error}]"
            )

            print(f"Error: {error}")

    def __find_task(self: sqlite3.SQLITE_SELECT) -> sqlite3.SQLITE_SELECT:
        """
        * Поиск задачи по сходимости задачи из файла todo.db (База данных).
        * Метод отвечает за уникальность задачи, если задача существует в таблице
        то метод вызывает исключения.
        * Метод вызывается автоматически в методе [-- add_task(self) --].

        Параметры:
        -----------
        отсутствует

        Возврат:
        ----------
        Метод возвращает задачу, если задача не встречалась в таблице.

        """

        # [1] Выбрать все имени задачи из файла todo.db.
        # [2] Итерировать в цикл for полученные имени задачи.
        for row in self.__cur.execute("""SELECT name FROM tasks"""):
            # [3] Если итерированная задача совпадёт с введённым задачей....
            if row[0] == self.__t_name:
                # Регистрировать ошибку в файл 'debug.log'.
                logger.error(
                    f"Описание: Повторение одинаковых задач не допускается.\n \
                        Введённая значения: [{self.__t_name}] \n \
                        Значения из БД: [{row[0]}]."
                )

                # [3.1] вызвать исключение с сообщением и прервать программу.
                raise NameExc(message="Задача с таким же именем уже существует!")

        # [4] Иначе возвращать имя задачи.
        return self.__t_name

    def __automat_delete_task(self: sqlite3.SQLITE_DELETE) -> sqlite3.SQLITE_DELETE:
        """
        * Метод отвечает за автоматическое удаление задачи из файла todo.db (База данных).
        * Метод удаляет задачи по дате и времени, для освобождения мест в таблице.
        * Метод вызывается автоматически в конструкторе [ __init__(self) ].

        Параметры:
        -------------
        отсутствует

        """

        # [1] Если дата не равно с текущим и ...
        # [2] время меньше или равно с текущим временем...
        # [3] удалить это запись.
        # * так как это задача является старым.
        self.__cur.execute(
            f"""DELETE  FROM tasks WHERE date != ? AND time_task <= ?""",
            (time.strftime("%d.%m.%Y"), time.strftime("%H:%M:%S")),
        )
        # [4] Сохранит изменение.
        self.__connection.commit()

    def show_tasks(self: sqlite3.SQLITE_SELECT) -> sqlite3.SQLITE_SELECT:
        """
        * Метод отвечает за вывод на экран все данные из файла todo.db (База данных)
        * Метод вызывается по необходимости/желанию пользователя.
        * Метод выводит на экран данные в виде таблицы:
        +----+---------------------+-----------+-----------------+------------------+
        | id |       задача        | приоритет | дата добавления | время добавления |
        +----+---------------------+-----------+-----------------+------------------+
        | 2  | do python exercises |    8     |    31.10.2022    |     14:21:20     |
        | 3  |       sleep         |    6     |    31.10.2022    |     14:23:00     |
        +----+---------------------+-----------+-----------------+------------------+

        Параметры:
        -------------
        отсутствует

        """

        # * Класс [-- PrettyTable() -- ] отвечает за красивый вывод информации в консоль.
        # [1] Создать объект класса [-- PrettyTable() -- ].
        table = PrettyTable()

        # [2] Вызвать метод [-- filed_names --] для создания заголовок таблицы.
        table.field_names = [
            "id",
            "задача",
            "приоритет",
            "дата добавления",
            "время добавления",
        ]

        # [3] Итерировать все данные из таблицы [-- tasks --].
        for id_task, name, priority, date, time_task in self.__cur.execute(
            """SELECT * FROM tasks"""
        ):
            # [3.1] Итерированные данные добавляются в строки таблицы [-- table --].
            table.add_row([id_task, name, priority, date, time_task])

        # [4] Вывод данные в виде таблицы, как указано в документации метода [-- show_tasks(self) --].
        success()
        print(table)

    def update_priority(self: sqlite3.SQLITE_UPDATE) -> sqlite3.SQLITE_UPDATE:
        """
        * Метод отвечает за изменение и обновление приоритета задачи в файле todo.db (База данных).
        * Метод вызывается по необходимости/желанию пользователя.

        Параметры:
        -----------
        отсутствует

        """

        # [1] Запрос приоритет задачи от пользователя.
        # [1.2] Проверка диапазон приоритета.
        priority = input("Укажите приоритет задачи: ").lower().strip()

        #  Если введённая значения является строкой или пустой значенией ...
        if priority.isalpha() == True or len(priority) == 0:
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл 'str' вместо 'int'.\n \
                        Введённая значения: [{priority}] --> 'str'\n \
                        Ожидаемая значения: [1, 2, 3, 4, ...] --> 'int'"
            )
            # Вызвать исключение с сообщением и прервать программу.
            raise TypeExc(message="'Приоритет' принимает только числовое значение!")

        # [1.3] Если приоритет задачи вне диапазона...
        elif int(priority) not in range(1, 11):
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл число вне диапозона. [1:10]\n \
                        Введённая значения: [{priority}] >= [1:10]\n \
                        Ожидаемая значения: [{priority}] <= [1:10] "
            )
            
            # [1.4] вызвать исключение с сообщением и прервать программу.
            raise PriorityExc(message="Указанный приоритет вне диапазона [1: 10]!")

        # [2] Запрос номер задачи от пользователя.
        id_num = input("Укажите номер задачи: ").lower().strip()

        #  Если введённая значения является строкой или пустой значенией ...
        if id_num.isalpha() == True or len(id_num) == 0:
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл 'str' вместо 'int'.\n \
                        Введённая значения: [{id_num}] --> 'str'\n \
                        Ожидаемая значения: [1, 2, 3, 4, ...] --> 'int'"
            )
            # Вызвать исключение с сообщением и прервать программу.
            raise TypeExc(message="'Номер задачи' принимает только числовое значение!")

        # [2.1] Если указанный номер задачи не существует в файле todo.db (База данных) в таблице (tasks)...
        if (
            int(id_num)
            not in self.__cur.execute("SELECT * FROM tasks WHERE id_task").fetchall()[0]
        ):
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл ID вне диапазона [1:15]\n \
                или ввёл не существующий ID."
            )

            # [2.2] вызвать исключение с сообщением и прервать программу.
            raise IdExc(
                message="Указанный ID не существует или вне диапазона [1 : 15]!!"
            )

        # [3] Изменение и обновление приоритет задачи.
        self.__cur.execute(
            """UPDATE tasks SET priority = ? WHERE id_task = ?""", (priority, id_num)
        )
        # [3.1] Сохранить обновлённую таблицу.
        self.__connection.commit()

    def delete_task(self: sqlite3.SQLITE_DELETE) -> sqlite3.SQLITE_DELETE:
        """
        * Метод отвечает за удаление задачи по id задачи из файла todo.db(База данных).
        * Метод вызывается по необходимости/желанию пользователя.

        Параметры:
        -----------
        отсутствует

        """

        # [1] Запрос номер задачи от пользователя.
        self.__id_num = input("Укажите номер задачи: ").lower().strip()
        # [1.2] Если указанный номер вне диапазона...

        #  Если введённая значения является строкой или пустой значенией ...
        if self.__id_num.isalpha() == True or len(self.__id_num) == 0:
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл 'str' вместо 'int'.\n \
                        Введённая значения: [{self.__id_num}] --> 'str'\n \
                        Ожидаемая значения: [1, 2, 3, 4, ...] --> 'int'"
            )
            # Вызвать исключение с сообщением и прервать программу.
            raise TypeExc(message="'Номер задачи' принимает только числовое значение!")

        elif (
            int(self.__id_num)
            not in self.__cur.execute("SELECT * FROM tasks WHERE id_task").fetchall()[0]
        ):
            # Регистрировать ошибку в файл 'debug.log'.
            logger.error(
                f"Описание: Пользователь ввёл ID вне диапазона [1:15]\n \
                или ввёл не существующий ID."
            )
            # [1.5] вызвать исключение с сообщением и прервать программу.
            raise IdExc(
                message="Указанный ID не существует или вне диапазона [1 : 15]!!"
            )

        # Удаление задачи по указанной id задачи.
        self.__cur.execute("""DELETE FROM tasks WHERE id_task = ?""", (self.__id_num,))

        # Сохранить изменение.
        self.__connection.commit()

    def close_connection(self):
        """
        * Метод отвечает за закрытие файла todo.db (База данных).
        * Метод вызывается по необходимости/желанию пользователя.

        Параметры:
        -----------
        отсутствует

        """

        print("Программа завершена!")
        self.__cur.close()
        self.__connection.close()


if __name__ == "__main__":
    print("[-- functions.py - запущен. --]")
else:
    print("[-- functions.py - импортирован. --]")
