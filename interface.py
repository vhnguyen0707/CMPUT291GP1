import datetime
import re
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

    def generateTicket(self):
        #   generate ticket by incrementing the highest current ticket ID
        query = "select  max(tno) from tickets"
        self.crsr.execute(query)
        tickets = self.crsr.fetchall()
        if len(tickets) == 0:
            return '0'
        return str(tickets[0][0]+1)

    def createTicket(self, info):
        if self.role != "o":
            print("you do not have the privilege to perform this operation")
            return False
        # TODO perform operation
        while (True):
            regno =  input("Please enter registration number: ")
            if regno != '':
                self.crsr.execute('''SELECT r.fname||' '|| r.lname, v.make, v.model, v.year, v.color
                FROM  registrations AS r, vehicles AS v 
                WHERE  r.regno = ? AND r.vin = v.vin;''', (regno,))
                regnoExists = self.crsr.fetchone()
                if regnoExists:
                    print(regnoExists[0])
                    prompt = input("Proceed to issue ticket? (Y/N): ").upper()
                    if prompt == 'N':
                        return False

                    elif prompt == 'Y':
                        # get ticket

                        ticket = self.generateTicket()

                        # get violation date
                        # if is not provided set violation date to current date

                        violationDate = input('Enter violation date (yyyy-mm-dd) or leave blank to get current date: ')
                        if violationDate =='':
                            violationDate = datetime.datetime.now().strftime("%Y-%m-%d")
                            print(violationDate)
                        while not datetime.datetime.strptime(violationDate, '%Y-%m-%d'):
                            print("Invalid date")
                            violationDate = input("Please re-enter violation date (yyyy-mm-dd): ")
                        violationText = input("Enter description of violation: ")
                        fineAmount = input("Enter fine amount: ")
                        data = (ticket, regno, fineAmount, violationText, violationDate)
                        self.crsr.execute("INSERT INTO tickets VALUES (?,?,?,?,?);", data)
                        self.connection.commit()
                        print("Successfully issued ticket\n")
                else:
                    print("Registration number does not exist\n")
                    again = input("Try again?(Y/N): ").upper()
                    if again == 'Y':
                        self.createTicket(info)
                    else:
                        return False


    def findOwner(self, info):
        if self.role != "o":
            print("you do not have the privilege to perform this operation")
            return False

        # TODO perform operation
        
        empty = 0
        query = '''
        SELECT v.make, v.model, v.year, v.color, r.plate, r.regdate, r.expiry, r.fname||' '||r.lname
        FROM vehicles as v, (select vin, plate, regdate, expiry, fname, lname 
                            from registrations r1 
                            where regdate >= (select max(regdate) from registrations r2 where r2.vin = r1.vin)) as r 
        WHERE v.vin = r.vin               
                '''
        iMake = input("Enter car make, or leave blank to pass: ")
        iModel = input("Enter car model, or leave blank to pass: ")
        iYear = input("Enter car year, or leave blank to pass: ")
        iColor = input("Enter car color, or leave blank to pass: ")
        iPlate = input("Enter car plate, or leave blank to pass: ")
        # incrementing the query if there is an input, otherwise, increment empty count.
        if iMake !='':
            query += " AND v.make ='{}'".format(iMake)
        else:
            empty += 1

        if iModel != '':
            query += " AND v.model = '{}'".format(iModel)
        else:
            empty += 1
        

        if iYear != '':
            query  += " AND v.year = '{}'".format(iYear)
        else:
            empty += 1
        

        if iColor != '':
            query += " AND v.color = '{}'".format(iColor)
        else: 
            empty += 1
        

        if iPlate != '':
            query += " AND r.plate = '{}'".format(iPlate)
        else:
            empty += 1
    
        if empty != 5 :
            query += ' COLLATE NOCASE ;'
            self.crsr.execute(query)
            info = self.crsr.fetchall()
            if not info:
                print("No cars found!")
            else:
# display all results and let user choose one car to see owner and info of registration
                if len(info) > 4:
                    print("|   make   |  model | year | color |  plate  |")
                    for car in info:
                        print("-"*63)
                        for col in range(5):
                            print("| ", end = '')
                            print(car[col], end ='')
                            print(" ", end ='')
                        print("|")
                    print("-"*63)
        
                    flag = 1
                    while flag:
                        selection = input("Select a car from 1 - {} to see more information:".format(len(info)))
                        if re.match("^[1-{}]*$".format(len(info)), selection):
                            # display owner of the chosen car
                            self.displayOwner([info[selection-1]])
                        else:
                            print("Invalid option!")
                            flag = 0
                else:
                    # display all if there are less then 4 cars matching input of user
                    self.displayOwner(info)
        else:
            again = input("Try again?(Y/N): ").upper()
            if again == 'Y':
                self.findOwner(info)
            else:
                return False            

    def displayOwner(self, data):
        print("|   make   |  model | year | color |  plate  |registrationDate|   expiry   |       owner       |")
        print("-"*100)
        for car in data:
            for col in range(8):
                print("| ", end='')
                print(car[col], end ='')
                print("  ", end = '')
            print("|")
            print("-"*100)










