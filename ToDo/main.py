from sys import path
from art import tprint
from loguru import logger
from packages.todo.main_menu import ru_main

path.append("..\\packages")


def main_menu():
    tprint("To Do List.")

    ru_main()


if __name__ == "__main__":
    print("[-- main.py - запущен. --]")
    main_menu()

else:
    print("[-- main.py - импортирован. --]")
