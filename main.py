import sqlite3
import login
from interface import Interface
from os import system as sys


def main():
    sys("clear")  # clear screen

    # establish connection to database upon starting the program
    try:
        connection = sqlite3.connect("testDB.db")
    except sqlite3.Error as e:
        print("unable to connect")
        exit(1)

    verified = login.verification(connection)

    # start CLI if verification is completed
    if verified[0]:
        cli = Interface(connection, verified[1])
        cli.start()

    # clear screen and print goodbye message before exiting
    sys("clear")
    print("Goodbye")
    connection.close()


if __name__ == '__main__':
    main()
