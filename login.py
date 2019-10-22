import sqlite3
from os import system as sys
from time import sleep

errorMsg = "username or password is invalid, please try again"

def verification(connection):
    while True:
        sys("clear")  # clear screen
        print("Welcome, please enter your credentials to login")
        print("if you wish to quit the program, press [return] 2 times")
        username = input("Username: ")  # ask for username
        password = input("Password: ")  # ask for password

        # check if user wants to exit
        if len(username) == 0:
            exit(0)

        # check if the input are in the right format, if not, display error message for 2sec, then restart
        if len(username) > 8 or len(password) > 8 or len(password) == 0:
            print(errorMsg)
            sleep(2)
            continue

        # create cursor
        crsr = connection.cursor()

        # fetch user's password for verification
        retData = crsr.execute("""SELECT pwd FROM users WHERE uid = ?""", (username,)).fetchall()

        # check if retData is empty, if so, display failed message for 2sec, then restart
        if not retData:
            print(errorMsg)
            sleep(2)
            continue

        # verify password
        if password == retData[0][0]:
            print("Verification Complete")
            return True, username
        else:
            print(errorMsg)
            sleep(2)
            continue


