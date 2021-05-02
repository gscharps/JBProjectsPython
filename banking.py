import sqlite3
import random


#set up db
class Database:
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
    def acct_exists(self, acct_num):
        self.cur.execute('select * from card where number=?', (str(acct_num),))
        return self.cur.fetchone()
    def validateCredentials(self, acct_num, pin):
        self.cur.execute('SELECT * FROM card WHERE number=? AND pin=?', (acct_num, pin))
        return self.cur.fetchone()
    def insert_acct(self, Account):
        #don't forget to commit after query
        self.cur.execute('INSERT INTO card VALUES (?, ?, ?, ?)', (Account.id, Account.number, Account.pin, Account.balance))
        self.conn.commit()
    def get_balance(self, acct_num):
        self.cur.execute('SELECT balance FROM card WHERE number=?', (acct_num,))
        balance = self.cur.fetchone()
        return balance[0]
    def set_balance(self, acct_num, balance):
        self.cur.execute('UPDATE card SET balance=? WHERE number=?', (balance, acct_num))
        self.conn.commit()
    def DeleteAccount(self, acct_num):
        #delete the account from the database
        self.cur.execute('DELETE FROM card WHERE number=?', (acct_num,))
        self.conn.commit()
    def increaseBalance(self, acct_num, amount):
        currBalance = self.get_balance(acct_num)
        newBalance = amount + currBalance
        self.set_balance(acct_num, newBalance)
    def reduceBalance(self, acct_num, amount):
        currBalance = self.get_balance(acct_num)
        newBalance = currBalance - amount
        self.set_balance(acct_num, newBalance)
    def TransferMoney(self, transfer):
        self.reduceBalance(transfer.from_acct, transfer.amount)
        self.increaseBalance(transfer.to_acct, transfer.amount)
    def close(self):
        self.conn.close()
class Account:
    def __init__(self, id, number, pin, balance):
        self.id = id
        self.number = number
        self.pin = pin
        self.balance = balance
class AccountGenerator:
    id_generator = 0
    minCardNumNoCheckSum = 400000010000000
    maxCardNumNoCheckSum = 400000019999999
    def CreateCardNum(self):
        randomCardNum = random.randint(self.minCardNumNoCheckSum, self.maxCardNumNoCheckSum)
        randomCardNum = (randomCardNum * 10) + self.check_sum(str(randomCardNum))
        return randomCardNum
    def CreateAccount(self):
        cardNum = self.CreateCardNum()
        newAcct = Account(self.id_generator, cardNum, random.randint(1000, 9999), 0)
        return newAcct
    def check_sum(self, cardNumNoCheckSum):
        digits = []
        for i in cardNumNoCheckSum:
            digits.append(int(i))
        for i in range(len(digits)):
            if (i+1) % 2 == 1:
                digits[i] *= 2
        for i in range(len(digits)):
            if digits[i] > 9:
                digits[i] -= 9
        sum = 0
        for i in digits:
            sum += i
        sum %= 10
        if 10 - sum == 0:
            return 0
        elif (10 - sum == 10):
            return 0
        else:
            retval = 10 - sum
            return retval
class Transfer:
    def __init__(self, from_acct, to_acct, amount):
        self.from_acct = from_acct
        self.to_acct = to_acct
        self.amount = amount
    def isValid(self, database):
         return self.EnoughMoney(database) and \
                self.DifferentAccounts()
    def LookupAccount(self, database, toAccount):
        if database.acct_exists(self.to_acct):
            return True
        else:
            print('Such a card does not exist')
            return False
    def EnoughMoney(self, database):
        curr_bal = database.get_balance(self.from_acct)
        if curr_bal < self.amount:
            print('Not enough money!')
            return False
        else:
            return True
    def DifferentAccounts(self):
        if self.from_acct == self.to_acct:
            print("You can't transfer money to the same account!")
            return False
        else:
            return True
class UserInterface:
    logged_in_user = None
    def main_menu(self):
        print('\n1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        return int(input())
    def sub_menu(self):
        print('1. Balance')
        print('2. Add Income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        return int(input())
    def GetTransferToAccount(self, database):
        toAccount = input('Enter card number:')
        # do check sum validation
        ag = AccountGenerator()
        check_sum = toAccount[-1]
        no_check_sum = toAccount[:15]
        if int(check_sum) == ag.check_sum(no_check_sum):
            return toAccount
        else:
            print('Probably you made a mistake in card number. Please try again!')
            return False
    def GetTransferAmount(self):
        return int(input('Enter how much money you want to transfer:'))
    def login(self, database, acct_num, pin):
        if (database.validateCredentials(acct_num, pin)):
            print('You have successfully logged in!')
            return True
        else:
            print('Wrong card number or PIN!')
            return False
    def log_out(self):
        print('You have successfully logged out!')
    def display_card_info(self, Acct):
        print('\nYou card has been created')
        print('Your card number:')
        print(Acct.number)
        print('Your card PIN:')
        print(Acct.pin)
    def getIncome(self):
        return int(input('Enter income:'))


UI = UserInterface()
db = Database()
main_menu_selection = UI.main_menu()
acct_generator = AccountGenerator()
sub_menu_selection = None

while main_menu_selection != 0:
    if main_menu_selection == 1:
        #create account
        newAcct = acct_generator.CreateAccount()
        while db.acct_exists(newAcct.number):
            newAcct = acct_generator.CreateAccount()
        db.insert_acct(newAcct)
        UI.display_card_info(newAcct)
        main_menu_selection = UI.main_menu()
        continue

    elif main_menu_selection == 2:
        #login
        number = input('\nEnter your card number:')
        pin = int(input('Enter your PIN:'))
        if UI.login(db, number, pin):

            sub_menu_selection = UI.sub_menu()
            while sub_menu_selection != 0:
                if sub_menu_selection == 1:
                    #balance
                    print('Balance: ' + str(db.get_balance(number)))
                    sub_menu_selection = UI.sub_menu()
                    continue
                elif sub_menu_selection == 2:
                    #add income
                    income = UI.getIncome()
                    db.increaseBalance(number, income)
                    print('Income was added!')
                    sub_menu_selection = UI.sub_menu()
                    continue
                elif sub_menu_selection == 3:
                    #Do transfer
                    transferTo = UI.GetTransferToAccount(db)
                    amount = 0
                    transfer = Transfer(number, transferTo, amount)
                    if transferTo and transfer.LookupAccount(db, transfer.to_acct):
                        transfer.amount = UI.GetTransferAmount()
                        if transfer.isValid(db):
                            db.TransferMoney(transfer)
                            print('Success!')
                    sub_menu_selection = UI.sub_menu()
                    continue
                elif sub_menu_selection == 4:
                    #close account
                    db.DeleteAccount(number)
                    print('The Account has been closed!')
                    break
                elif sub_menu_selection == 5:
                    #log out
                    UI.log_out()
                    break
    if sub_menu_selection == 0:
        #exit
        main_menu_selection = 0
    else:
        main_menu_selection = UI.main_menu()
print('Bye!')

db.close()

