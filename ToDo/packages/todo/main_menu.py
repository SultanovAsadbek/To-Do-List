from packages.todo.menu_controller import controller


def ru_main():
    """
    * Функция не имеет параметров.
    * Функция предоставляет пользователю меню команд,
    полученную команду передаёт
    в функцию [-- controller() --] в качестве аргумента.

    Ключевые аргументы:
    -------------------
    аргументы отсутствуют.

    Возврат:
    ------------
    True
        При удачном выполнении.
    False
        При завершении работы

    """

    while True:
        print(
            f"\n\n{'-' * 30}"
            f"\n|--- [1]: Показать задачи дня."
            f"\n|--- [2]: Добавить задачи."
            f"\n|--- [3]: Изменить приоритет."
            f"\n|--- [4]: Удалить задачу."
            f"\n|\n|--- [exit]/[0]: Выход."
            f"\n{'-' * 30}"
        )

        command = input("Выберите команду: ")
        if command in ("0", "exit"):
            controller(command)
            return False

        controller(command)


if __name__ == "__main__":
    print("[-- main_menu.py - запущен. --]")
    ru_main()
else:
    print("[-- main_menu.py - импортирован. --]")
