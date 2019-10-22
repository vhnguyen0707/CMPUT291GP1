class Interface:
    def __init__(self, connection, username):
        self.crsr = connection.cursor()
        self.username = username
        retData = self.crsr.execute("""SELECT utype FROM users WHERE uid = ?""", (self.username,)).fetchall()
        self.role = retData[0][0]

    def start(self):
        while True:
            command = input("Command: ")
            command_parsed = self.cmdParser(command)


    def cmdParser(self, command):
        '''
        commands:
            regBirth    fname, lname, gender, birthDate, birthPlace, fnameMother, lnameMother, fnameFather, lnameFather
            regMar      fnameP1, lnameP1, fnameP2, lnameP2,
            renewVReg
            procSale
            procPay
            getAbstract
            createTicket
            findOwner
        '''

    def regBirth(self, info):
        pass

    def regMar(self, info):
        pass

    def renewVReg(self, info):
        pass

    def procSale(self, info):
        pass

    def procPay(self, info):
        pass

    def getAbstract(self, info):
        pass

    def createTicket(self, info):
        pass

    def findOwner(self, info):
        pass

