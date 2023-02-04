class NameExc(Exception):
    """
    Класс исключения --NameException--
    Класс вызывается в случи если:
        * текст задачи состоит из пробелов
        * количество букв в тексте задачи меньше 7
        * текст задачи уже существует
            в таблице [-- tasks --] в файле [-- todo.db (База данный) --]
        * поле задачи пуст

    Аттрибуты:
    -------------
    head : str
        заголовок
    message : str
        сообщение о конкретном ошибке.

    """

    def __init__(self, head="ToDoTaskNameError", message="Bad name!"):
        super().__init__(message)
        self.head = head
        self.message = message


class PriorityExc(Exception):
    """
    Класс исключение --PriorityException--
    Класс вызывается в случи если:
        * приоритет задачи вне диапазона [1:10]

    Аттрибуты:
    -------------
    head : str
        заголовок
    message : str
        сообщения об конкретном ошибке

    """

    def __init__(self, head="ToDoTaskExcError", message="Bad priority!"):
        super().__init__(message)
        self.head = head
        self.message = message


class IdExc(Exception):
    """
    Класс исключение --IdException--
    Класс вызывается в случи если:
        * введённое пользователем id не существует
           в таблице [-- tasks --] в файле [-- todo.db (База данный) --]
        * введённое пользователем id вне диапазона [1:15]
        * количество задачи больше
           в таблице [-- tasks --] в файле [-- todo.db (База данный) --]

    Аттрибуты:
    -------------
    head : str
        заголовок
    message : str
        сообщения об конкретном ошибке

    """

    def __init__(self, head="ToDoTaskIdError", message="Bad ID!"):
        super().__init__(message)
        self.head = head
        self.message = message


class TypeExc(Exception):
    """
    Класс исключение --TypeException--
    Класс вызывается в случи если:
        * пользователи введут строку вместо цифры.
        * пользователи ничего не введут (пустая строка).

    Аттрибуты:
    -------------
    head : str
        заголовок
    message : str
        сообщения об конкретном ошибке

    """

    def __init__(self, head="ToDoTaskTypeError", message="Bad Type!"):
        super().__init__(message)
        self.head = head
        self.message = message


if __name__ == "__main__":
    print("[-- exceptions.py - запущен. --]")
else:
    print("[-- exceptions.py - импортирован. --]")
