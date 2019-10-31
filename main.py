import sqlite3
from os import system as sys
from time import sleep

import login
from interface import Interface


def main():
    sys("clear")  # clear screen
    # establish connection to database upon starting the program
    try:
        print("Connecting to Database...", end="")
        connection = sqlite3.connect("testDB1.db")
    except sqlite3.Error:
        print("unable to connect to database")
        exit(1)
    sleep(1)
    print("Connected")
    sleep(1)
    sys("clear")

    # verify identity, verified is a list
    # verified[0] is True/False indicating if the user has verified his identity
    # verified[1] is the username
    # verified[2] is the role
    # verified[3] is the city
    verified = login.verification(connection)

    # start CLI if verification is completed
    sys("clear")
    if verified[0]:
        cli = Interface(connection, verified[1].lower(), verified[2].lower(), verified[3].lower())
        cli.start()

    # clear screen and print goodbye message before exiting
    sys("clear")
    print("Goodbye")
    connection.close()
    exit(0)


if __name__ == '__main__':
    main()
