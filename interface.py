import datetime
import sqlite3
import random



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
            command = input("Command: ").split(" ")  # get command
            command = [x for x in command if x != ""]  # remove empty entry from command
            command[0] = command[0].lower()

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

        firstname = info[1]
        lastname = info[2]
        gender = info[3]
        bdate = info[4]
        bplace = info[5]
        fnameMother = info[6]
        lnameMother = info[7]
        fnameFather = info[8]
        lnameFather = info[9]

        # get regdate
        register_date = str(datetime.datetime.now().date())

        # This is for creating the unique regno
        register_number = None
        while True:
            register_number = random.randint(4000, 5000000000)
            retData = self.crsr.execute('''select * from births WHERE regno = ? COLLATE NOCASE''', (register_number,)).fetchall()
            if not retData:
                break
            else:
                continue

        # this is a tuple that contains the infromation of the new born
        atuple = (register_number, firstname, lastname, register_date, self.city,
                  gender, fnameFather, lnameFather, fnameMother,
                  lnameMother)
        # this part is to add the infromation into table births
        self.crsr.execute('''insert into births values (?,?,?,?,?,?,?,?,?,?);''', atuple)
        self.connection.commit()

        mother_name = (fnameMother, lnameMother)
        # to check wether the table persons contains the parents information about the now born
        mom_addr_phone = self.crsr.execute('''select address, phone from persons where fname = ? COLLATE NOCASE and lname = ? COLLATE NOCASE''', mother_name).fetchall()
        if not mom_addr_phone:
            mother_bdate = input("Enter mother's birth date \n")
            mother_bplace = input("Enter mother's birth place \n")
            mother_address = input("Enter mother's address \n")
            mother_phone = input("Enter mother's phone number \n")

            if mother_bdate == '':
                mother_bdate = 'NULL'
            if mother_bplace == '':
                mother_bplace = 'NULL'
            if mother_address == '':
                mother_address = 'NULL'
            if mother_phone == '':
                mother_phone = 'NULL'

            alist = (fnameMother, lnameMother, mother_bdate, mother_bplace, mother_address, mother_phone)
            self.crsr.execute('''insert into persons values (?,?,?,?,?,?);''', alist)
            self.connection.commit()

        else:
            # add the new birth information into table persons
            mother_address = mom_addr_phone[0][0]
            mother_phone = mom_addr_phone[0][1]
        atuple3 = (firstname, lastname, bdate, bplace, mother_address, mother_phone)
        self.crsr.execute('''insert into persons values(?,?,?,?,?,?);''', atuple3)
        self.connection.commit()
        
        
        
        # ask for father's info if father does not exist in the databse
        atuple = (fnameFather, lnameFather)
        retData = self.crsr.execute('''select persons.fname , persons.lname from persons where fname = ? COLLATE NOCASE and lname = ? COLLATE NOCASE''', atuple).fetchall()
        if not retData:
            father_bdate = input("Enter father's birth date \n")
            father_bplace = input("Enter father's birth place \n")
            father_address = input("Enter father's address \n")
            father_phone = input("Enter father's phone number \n")

            if father_bdate == '':
                father_bdate = 'NULL'
            if father_bplace == '':
                father_bplace = 'NULL'
            if father_address == '':
                father_address = 'NULL'
            if father_phone == '':
                father_phone = 'NULL'
            alist = (fnameFather, lnameFather, father_bdate, father_bplace, father_address, father_phone)
            self.crsr.execute('''insert into persons values (?,?,?,?,?,?);''', alist)
            self.connection.commit()
        
        
        print("New Birth Record added")
        return True

    def regMar(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        partner1_firstname = info[1]
        partner1_lastname = info[2]
        partner2_firstname = info[3]
        partner2_lastname = info[4]
        register_place = self.city

        # generate a new unique regno
        register_number = None
        while True:
            register_number = random.randint(4000, 5000000000)
            retData = self.crsr.execute("""SELECT * FROM registrations WHERE regno = ? COLLATE NOCASE""",
                                        (register_number,)).fetchall()
            if not retData:  # the newRegno is unique
                break
            else:  # the newRegno is not unique
                continue

        atuple = (register_number, datetime.datetime.now().date(), register_place,
                  partner1_firstname, partner1_lastname, partner2_firstname, partner2_lastname)

        # this part is to add the information into table marriages
        self.crsr.execute('''insert into marriages values (?,?,?,?,?,?,?);''', atuple)
        self.connection.commit()

        # check if a person already exist in the database
        partner1_info = (partner1_firstname, partner1_lastname)
        self.crsr.execute('''select * from persons where fname = ? COLLATE NOCASE and lname = ? COLLATE NOCASE''', partner1_info)
        partner1_name = self.crsr.fetchall()

        if not partner1_name:
            partner1_bdate = input("Enter the partner1's birth date \n")
            partner1_bplace = input("Enter the partner1's birth place \n")
            partner1_address = input("Enter your partner1's address \n")
            partner1_phone = input("Enter your partner1's phone number \n")

            if partner1_bdate == '':
                partner1_bdate = "NULL"
            if partner1_bplace == '':
                partner1_bplace = "NULL"
            if partner1_address == '':
                partner1_address = "NULL"
            if partner1_phone == '':
                partner1_phone = "NULL"

            alist = (partner1_firstname, partner1_lastname, partner1_bdate, partner1_bplace,
                     partner1_address, partner1_phone)
            self.crsr.execute('''insert into persons values(?,?,?,?,?,?)''', alist)
            self.connection.commit()

        partner2_info = (partner2_firstname, partner2_lastname)
        self.crsr.execute('''select fname,lname from persons where fname = ? COLLATE NOCASE and lname = ? COLLATE NOCASE''', partner2_info)
        partner2_name = self.crsr.fetchall()
        if not partner2_name:
            partner2_bdate = input("Enter the partner2's birth date \n")
            partner2_bplace = input("Enter the partner2's birth place \n")
            partner2_address = input("Enter your partner2's address \n")
            partner2_phone = input("Enter your partner2's phone number \n")

            if partner2_bdate == '':
                partner2_bdate = "NULL"
            if partner2_bplace == '':
                partner2_bplace = "NULL"

            if partner2_address == '':
                partner2_address = "NULL"

            if partner2_phone == '':
                partner2_phone = "NULL"

            atuple = (partner2_firstname, partner2_lastname, partner2_bdate,
                      partner2_bplace, partner2_address, partner2_phone)
            self.crsr.execute('''insert into persons values (?, ?, ?, ?, ?, ?)''', atuple)
            self.connection.commit()

        self.connection.commit()

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

        # if the registration is already expired, set newExpirationDate to 1 year from currentDate
        if expirationDate < currentDate:
            newExpirationDate = datetime.date(currentDate.year + 1, currentDate.month, currentDate.day)
        elif expirationDate >= currentDate:  # else, add 1 year to expirationDate
            newExpirationDate = datetime.date(expirationDate.year + 1, expirationDate.month, expirationDate.day)

        # upload new date
        self.crsr.execute("""UPDATE registrations SET expiry = ? WHERE regno = ? COLLATE NOCASE""", (newExpirationDate, info[1],))
        self.connection.commit()  # commit the change

        # prompt changes
        print("Expiration Date for Registration %d set to: %s" % (int(info[1]), str(newExpirationDate)))

        return True

    def procSale(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        if len(info) != 7:
            print("Argument error, Please try again")
            return False
        # extract info
        vin = info[1].upper()
        co_fname = info[2]  # co = current owner
        co_lname = info[3]
        no_fname = info[4]  # no = new owner
        no_lname = info[5]
        plate = info[6].upper()

        # pull data from database
        retData = self.crsr.execute("""SELECT * FROM registrations WHERE vin = ? COLLATE NOCASE ORDER BY regdate DESC LIMIT 1""", (vin,)).fetchall()

        if retData:
            # verify current owner
            if retData[0][5].lower() == co_fname.lower() and retData[0][6].lower() == co_lname.lower():  # verification success
                # set old reg to expire today
                expireQuery = """UPDATE registrations 
                                 SET expiry = ? 
                                 WHERE vin = ? COLLATE NOCASE 
                                 AND fname = ? COLLATE NOCASE 
                                 AND lname = ? COLLATE NOCASE"""
                self.crsr.execute(expireQuery, (str(datetime.datetime.now().date()), vin, co_fname, co_lname,))
                self.connection.commit()  # commit the change

                # generate a new unique regno
                newRegno = None
                while True:
                    newRegno = random.randint(4000, 5000000000)
                    retData = self.crsr.execute("""SELECT * FROM registrations WHERE regno = ? COLLATE NOCASE""", (newRegno,)).fetchall()
                    if not retData:  # the newRegno is unique
                        break
                    else:  # the newRegno is not unique
                        continue

                # generate new regDate
                newRegDate = datetime.datetime.now().date()

                # generate new expiration date
                newExpirationDate = datetime.date(newRegDate.year + 1, newRegDate.month, newRegDate.day)

                # create new reg for the new owner
                newOwnerQuery = """INSERT INTO registrations VALUES (?, ?, ?, ?, ?, ?, ?)"""
                self.crsr.execute(newOwnerQuery, (newRegno, newRegDate, newExpirationDate, plate, vin, no_fname, no_lname,))
                self.connection.commit()  # commit the change

                # prompt success
                print("Sale Processed")
                return True
            else:  # verification failed
                print("The current owner recorded does not match the current owner supplied in the operation argument")
                print("Please verify your information and try again")
                return False
        else: # did not find the vin in the database
            print("Vehicle cannot be found in the system, please verify your information and try again")
            return False

    def procPay(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        tno = input("Please enter ticket number: " )
        tno_list = (tno,)

        # get the todays date
        currentdate = str(datetime.datetime.now().date())

        amount = 0
        try:
            amount = input("Please enter amount of payment: ")
        except ValueError:
            print("Payment Amount entered is invalid, Please try again")
            return False


        alist = (tno, currentdate, amount)
        ticket_num = (tno,)

        # this part is check wether the amount the user input is greater than fine
        self.crsr.execute('''select fine from tickets  where tno=?''', ticket_num)
        fine = self.crsr.fetchall()

        if fine:
            while True:
                if int(amount) > int(fine[0][0]):
                    print("Payment cannot exceed the fine amount")
                    amount = input("Please try again: ")
                else: 
                    break
            
            self.crsr.execute(''' select max(pdate) from payments where tno = ? ;''', ticket_num)
            pdate = self.crsr.fetchall()
            if pdate[0][0] == None:
                self.crsr.execute('''insert into payments values(?, ?, ?);''', alist)
                self.connection.commit()  
                print("Payment successful")
                
            else:
                if currentdate == pdate[0][0]:
                    print("You cannot make payment to a ticket twice on the same day!")
                else:
                    self.crsr.execute('''select sum(amount) from payments where tno = ? ;''', ticket_num)
                    paid = self.crsr.fetchall() 
                    sum_amount = int(amount) + int(paid[0][0])
                    if sum_amount > int(fine[0][0]):
                        print("The sum of payment exceeds the fine amount")
                    else:
                        self.crsr.execute('''insert into payments values(?, ?, ?);''', alist)
                        self.connection.commit()  
                        print("Payment successful")
                        
        
        else:
            print("the tno is not in table tickets so the payment can not be proceed")
            again = input("Try again?(Y/N): ").upper()
            if again == 'Y':
                self.createTicket(info)
            else:
                return False
                    
            
        # this part is to check wether the tno is in tickets or not
        #rows = self.crsr.execute('''select tno from tickets where tno = ? ;''', ticket_num).fetchall()

        #if not rows:

    def getAbstract(self, info):
        if self.role != "a":
            print("you do not have the privilege to perform this operation")
            return False

        # extract info
        fname = info[1]
        lname = info[2]

        # get number of tickets
        findTicketCountQuery = '''SELECT COUNT(*) 
                             FROM tickets JOIN registrations on tickets.regno = registrations.regno 
                             WHERE fname = ? COLLATE NOCASE
                             AND lname = ? COLLATE NOCASE'''
        retData = self.crsr.execute(findTicketCountQuery, (fname, lname, )).fetchall()
        ticketCount = retData[0][0]

        # get number of demerit notice
        findDemeritCountQuery = '''SELECT COUNT(*)
                                   FROM demeritNotices
                                   WHERE fname = ? COLLATE NOCASE
                                   AND lname = ? COLLATE NOCASE'''
        retData = self.crsr.execute(findDemeritCountQuery, (fname, lname,)).fetchall()
        demeritCount = retData[0][0]

        # total number of demerit points received within the past two years
        past2yearDemeritCountQuery = '''SELECT IFNULL(SUM(points),0)
                                   FROM demeritNotices
                                   WHERE fname = ? COLLATE NOCASE
                                   AND lname = ? COLLATE NOCASE
                                   AND ddate >= DATE('NOW', '-2 YEAR')'''
        retData = self.crsr.execute(past2yearDemeritCountQuery, (fname, lname,)).fetchall()
        past2yearDemeritCount = retData[0][0]

        # total number of demerit points received in lifetime
        lifetimeDemeritCountQuery = '''SELECT IFNULL(SUM(points),0)
                                   FROM demeritNotices
                                   WHERE fname = ? COLLATE NOCASE
                                   AND lname = ? COLLATE NOCASE'''
        retData = self.crsr.execute(lifetimeDemeritCountQuery, (fname, lname,)).fetchall()
        lifetimeDemeritCount = retData[0][0]

        # print abstract
        print("Ticket Count: %d" % ticketCount)
        print("Demerit Notice Count: %d" % demeritCount)
        print("Demerit Points (past 2 years): %d" % past2yearDemeritCount)
        print("Demerit Points (lifetime): %d" % lifetimeDemeritCount)

        # prompt user if they want to see the ticket
        choice = input("Would you like to see the details of each ticket? (Y/n): ")
        if choice.lower() == 'y':
            # print the 5 most recent ticket
            getTicketsQuery = '''SELECT tno, vdate, violation, fine, tickets.regno, make, model
                                 FROM tickets JOIN 
                                     (registrations JOIN vehicles v on registrations.vin = v.vin) on tickets.regno = registrations.regno
                                 WHERE fname = ? COLLATE NOCASE
                                 AND lname = ? COLLATE NOCASE
                                 ORDER BY vdate DESC
                                 LIMIT 5'''
            retData = self.crsr.execute(getTicketsQuery, (fname, lname,)).fetchall()
            print(" Ticket Number | Violation Date |   Violation   | Fine Amount | Registration Number |   Make   |   Model   ")
            for i in retData:
                a = "{:<15}".format(i[0])
                b = "{:<16}".format(i[1])
                c = "{:<15}".format(i[2])
                d = "{:<13}".format(i[3])
                e = "{:<21}".format(i[4])
                f = "{:<10}".format(i[5])
                g = "{:<11}".format(i[6])
                print(" " + a, end=' ')
                print(b, end=' ')
                print(c, end=' ')
                print(d, end=' ')
                print(e, end=' ')
                print(f, end=' ')
                print(g, end=' ')
        else:
            return True


    def generateTicket(self):
        #   generate ticket by incrementing the highest current ticket ID
        query = "select  max(tno) from tickets"
        self.crsr.execute(query)
        tickets = self.crsr.fetchall()
        if tickets[0][0] == None:
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
                    print("     Owner     |     Make     |     Model     |     Year     |     Color    ")
                    print("-"*75)
                    for i in range(len(regnoExists)):
                        print(regnoExists[i], end='')
                        print(' '*7, end='')
                    
                    prompt = input("\nProceed to issue ticket? (Y/N): ").upper()
                    if prompt == 'N':
                        break

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
                        break
                else:
                    print("Registration number does not exist\n")
                    break
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
        SELECT make, model, year, color, plate, regdate, expiry, fname||' '||lname
        FROM vehicles LEFT OUTER JOIN (select vin, plate, regdate, expiry, fname, lname 
                            from registrations r1 
                            where regdate >= (select max(regdate) from registrations r2 where r2.vin = r1.vin)) using (vin)
        WHERE '1' = '1'              
                '''
        # set first condition that is always true to concatenate AND condition
        iMake = input("Enter car make, or leave blank to pass: ")
        iModel = input("Enter car model, or leave blank to pass: ")
        iYear = input("Enter car year, or leave blank to pass: ")
        iColor = input("Enter car color, or leave blank to pass: ")
        iPlate = input("Enter car plate, or leave blank to pass: ")
        # incrementing the query if there is an input, otherwise, increment empty count.
        if iMake !='':
            query += " AND make = '{}' COLLATE NOCASE".format(iMake)
        else:
            empty += 1

        if iModel != '':
            query += " AND model = '{}' COLLATE NOCASE".format(iModel)
        else:
            empty += 1
        

        if iYear != '':
            query  += " AND year = '{}' COLLATE NOCASE".format(iYear)
        else:
            empty += 1
        

        if iColor != '':
            query += " AND color = '{}' COLLATE NOCASE".format(iColor)
        else: 
            empty += 1
        

        if iPlate != '':
            query += " AND plate = '{}' COLLATE NOCASE".format(iPlate)
        else:
            empty += 1
    
        if empty != 5 :
            query += ';'
            self.crsr.execute(query)
            info = self.crsr.fetchall()
            if not info:
                print("No cars found!")
            else:
# display all results and let user choose one car to see owner and info of registration
                if len(info) >= 4:
                    print("   make   |  model | year | color |  plate  ")
                    for car in info:
                        print("-"*63)
                        for col in range(5):
                            print("| ", end = '')
                            print(car[col], end ='')
                            print(" ", end ='')
                        print("|")
                    print("-"*63)
        
                    while True:
                        selection = input("Select a car from 1 - {} to see more information: ".format(len(info))).strip('\n')
                        if self.isInt(selection):
                            selection = int(selection)
                            if selection in range(1, len(info)):
                            # display owner of the chosen car
                                self.displayOwner([info[selection-1]])
                                break
                            else:
                                print("Invalid option!")
                        else:
                            print("Invalid option!")
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
        if len(data) == 1 and data[0][5] == None:
                print("\nThis car has no owner\n\n.")
        
        print("|   make   |  model | year | color |  plate  |registrationDate|   expiry   |       owner       |")
        print("-"*100)
        for car in data:
            for col in range(8):
                print("| ", end='')
                print(car[col], end ='')
                print("  ", end = '')
            print("|")
            print("-"*100)
                
    def isInt(self, selection):
        try:
            selection = int(selection)
            return True
        except:
            return False










