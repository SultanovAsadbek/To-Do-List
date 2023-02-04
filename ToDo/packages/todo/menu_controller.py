import time

from packages.todo.beatiful import success
from packages.todo.beatiful import failed
from packages.todo.beatiful import finish_programm
from packages.todo.beatiful import console

from packages.todo.functions import ToDo
from packages.todo.exceptions import NameExc
from packages.todo.exceptions import IdExc
from packages.todo.exceptions import PriorityExc
from packages.todo.exceptions import TypeExc


def controller(command):
    """
    * В функции вызывается класс [-- ToDo --]
    * Функция вызывает объект класса
        по соответствующим командам.

    Ключевые аргументы:
    --------------------
    аргумент [command] : команды (1, 2, 3, 4, 0/exit)
    тип: str

    Возврат:
    ----------
    Функция без возврата.

    """

    task = ToDo()
    if command == "1":
        console.print(f"\n{'-'*15} Просмотр задачи {'-'*15}", style="menu")
        task.show_tasks()
        time.sleep(2.5)

    # ------------ Добавить задачу ------------ #
    elif command == "2":
        try:
            console.print(f"\n{'-'*15} Добавление задачи {'-'*15}", style="menu")
            print(f"|-- Внимание!" f"\n|-- Диапазон приоритета [1:10]" f"\n|-- ")
            task.add_task()

        except (NameExc, PriorityExc, IdExc, TypeExc) as error:
            failed()
            console.print(f"Error: {error}", style="error")

        else:
            success()
            console.print("Задача успешно добавлена!", style="success")
            time.sleep(2.5)
        finally:
            print("\n")

    # ------ Изменение приоритет задачи ------ #
    elif command == "3":
        try:
            console.print(
                f"\n{'-'*15} Изменение приоритет задачи {'-'*15}", style="menu"
            )
            task.update_priority()

        except (NameExc, PriorityExc, IdExc, TypeExc) as error:
            failed()
            console.print(f"Error: {error}", style="error")

        else:
            success()
            console.print("Приоритет успешно изменён!", style="success")
            time.sleep(2.5)
        finally:
            print("\n")

    # ------------ Удалить задачу ------------ #
    elif command == "4":
        try:
            console.print(f"\n{'-'*15} Удаление задачи {'-'*15}", style="menu")
            task.delete_task()

        except (NameExc, PriorityExc, IdExc, TypeExc) as error:
            failed()
            console.print(f"Error: {error}", style="error")

        else:
            success()
            console.print("Задача успешно удалена!", style="success")
            time.sleep(2.5)
        finally:
            print("\n")

    # ------------ Выход из программы, закрытие базы данных ------------ #
    elif command in ("0", "exit"):
        finish_programm()
        task.close_connection()

    # ------ Не опознанная команда ------ #
    else:
        console.print("Команда не найдена!", style="error")


if __name__ == "__main__":
    print("[-- menu_controller.py - запущен. --]")
else:
    print("[-- menu_controller.py - импортирован. --]")
