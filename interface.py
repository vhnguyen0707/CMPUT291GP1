import datetime
import sqlite3
from os import system as sys


# print out a list of all commands and a short description for each
def help():
    info = ("Possible Command:",
            "   - regBirth          register a birth",
            "           arguments: fname, lname, gender, bdate, bplace, fnameMother, lnameMother, fnameFather, lnameFather",
            " ",
            "   - regMar            register a marriage",
            "           arguments: fnameP1, lnameP1, fnameP2, lnameP2",
            " ",
            "   - renewVReg         renew a vehicle registration",
            "           arguments: regNumber",
            " ",
            "   - procSale          process a sale",
            "           arguments: vin, fnameSaler, lnameSaler, fnameBuyer, lnameBuyer, newPlateNumber",
            " ",
            "   - procPay           process a payment",
            "           arguments: ticketNumber, amount",
            " ",
            "   - getAbstract       obtain driver abstract",
            "           arguments: fname, lname",
            " ",
            "   - createTicket      issue a ticket",
            " ",
            "   - findOwner         find a car's owner",
            " ",
            "   - quit              quit the program")
    for i in info:
        print(i)


class Interface:
    def __init__(self, connection, username, role, city):
        self.crsr = connection.cursor() # create cursor

        #user information
        self.username = username
        self.role = role
        self.city = city

        # a list of valid commands
        self.validCommand = ("regbirth", "regmar", "renewvreg",
                             "procsale", "procpay", "getabstract",
                             "createticket", "findowner", "help", "quit")

    def start(self):
        while True:
            print("")  # print a blank line
            command = input("Command: ").lower().split(" ")  # get command
            command = [x for x in command if x != ""]  # remove empty entry from command

            if command[0] in self.validCommand:  # check if command is valid
                if command[0] == "help" or command == "h":
                    help()
                elif command[0] == "quit" or command == "q":
                    break  # exit
                elif command[0] == "regbirth".lower():
                    self.regBirth(command[1:])
                elif command[0] == "regmar".lower():
                    self.regMar(command[1:])
                elif command[0] == "renewvreg".lower():
                    self.renewVReg(command[1:])
                elif command[0] == "procsale".lower():
                    self.procSale(command[1:])
                elif command[0] == "procpay".lower():
                    self.procPay(command[1:])
                elif command[0] == "getabstract".lower():
                    self.getAbstract(command[1:])
                elif command[0] == "createticket".lower():
                    self.createTicket(command[1:])
                elif command[0] == "findowner".lower():
                    self.findOwner(command[1:])
            else:  # prompt that an invalid command has been entered
                print("\"%s\" is not a valid command, type \"help\" for assistance" % " ".join(command))

    def regBirth(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation

    def regMar(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation

    def renewVReg(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation

    def procSale(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation

    def procPay(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation

    def getAbstract(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation

    def createTicket(self, info):
        if self.role != "o":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation

    def findOwner(self, info):
        if self.role != "o":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation

