import datetime
import sqlite3


# print out a list of all commands and a short description for each
def help():
    info = ("Possible Commands:",
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
            "   - quit              quit the program",
            " ",
            "Example Usage: regBirth Kylo Ren male 2019-01-24 edmonton Princess Leia Han Solo")
    for i in info:
        print(i)


class Interface:
    def __init__(self, connection, username, role, city):
        self.crsr = connection.cursor()  # create cursor

        self.connection = connection

        # user information
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
                elif command[0] == "regbirth":
                    self.regBirth(command)
                elif command[0] == "regmar":
                    self.regMar(command)
                elif command[0] == "renewvreg":
                    self.renewVReg(command)
                elif command[0] == "procsale":
                    self.procSale(command)
                elif command[0] == "procpay":
                    self.procPay(command)
                elif command[0] == "getabstract":
                    self.getAbstract(command)
                elif command[0] == "createticket":
                    self.createTicket(command)
                elif command[0] == "findowner":
                    self.findOwner(command)
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

        # fetch expiry date from db
        retData = self.crsr.execute("""SELECT expiry FROM registrations WHERE regno = ? COLLATE NOCASE""", (info[1],)).fetchall()
        # check if a valid regno was provided, if not, prompt and return
        if not retData:
            print("The provided regno could not be found in the database, please try again.")
            return
        # convert expiry date from db into python datetime object
        expirationDate = datetime.date(int(retData[0][0][0:4]), int(retData[0][0][5:7]), int(retData[0][0][8:10]))
        # get current date
        currentDate = datetime.datetime.now().date()
        # new date to be uploaded to the db
        newExpirationDate = None

        # if the registration is already expired, set newExpirationDate to 1 year from cuurentDate
        if expirationDate < currentDate:
            newExpirationDate = datetime.date(currentDate.year + 1, currentDate.month, currentDate.day)
        elif expirationDate >= currentDate: # else, add 1 year to expirationDate
            newExpirationDate = datetime.date(expirationDate.year + 1, expirationDate.month, expirationDate.day)

        # upload new date
        self.crsr.execute("""UPDATE registrations SET expiry = ? WHERE regno = ? COLLATE NOCASE""", (newExpirationDate, info[1],))
        self.connection.commit()  # commit the change

        print("Expiration Date for Registration %d set to: %s" % (int(info[1]), str(newExpirationDate)))

        return True

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

