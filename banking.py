import sqlite3
import random


#set up db
class Database:
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
    def acct_exists(self, acct_num, pin):
        self.cur.execute('SELECT * FROM card WHERE number=? AND pin=?', (acct_num, pin))
        if self.cur.fetchone():
            return True
        else:
            return False
    def insert_acct(self, Account):
        #don't forget to commit after query
        self.cur.execute('INSERT INTO card VALUES (?, ?, ?, ?)', (Account.id, Account.number, Account.pin, Account.balance))
        self.conn.commit()
    def get_balance(self, acct_num):
        self.cur.execute('SELECT balance FROM card WHERE number=?', acct_num)
        balance = cur.fetchone()
        return balance
    def close(self):
        self.conn.close()

#cur.execute('SELECT pin FROM card WHERE number=:num', {"num": Account.acct_num})
#print(cur.fetchone())

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
        newAcct = Account(self.id_generator, cardNum, 1111, 0)
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

class UserInterface:
    logged_in_user = None
    def main_menu(self):
        print('\n1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        return int(input())
    def logged_in_menu(self):
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')
        return int(input())
    def login(self, database, acct_num, pin):
        if (database.acct_exists(acct_num, pin)):
            return True
        else:
            return False
    def display_card_info(self, Acct):
        print('\nYou card has been created') 
        print('Your card number:')
        print(Acct.number)
        print('Your card PIN:')
        print(Acct.pin)

UI = UserInterface()
db = Database()
choice = UI.main_menu()
acct_generator = AccountGenerator()

while choice != 0:
    if choice == 1:
        newAcct = acct_generator.CreateAccount()
        while db.acct_exists(newAcct.number, newAcct.pin):
            newAcct = acct_generator.CreateAccount()
        db.insert_acct(newAcct)
        UI.display_card_info(newAcct)
        choice = UI.main_menu()
        continue

    elif choice == 2:
        number = int(input('\nEnter your card number:'))
        pin = int(input('Enter your PIN:'))
        if UI.login(db, number, pin):
            print('You have successfully logged in!')
            logged_in_choice = UI.logged_in_menu()
            while logged_in_choice != 0:
                if logged_in_choice == 1:
                    print('Balance: ' + str(db.get_balance(acct_num)))
                    logged_in_choice = UI.logged_in_menu()
                    continue
                elif logged_in_choice == 2:
                    print('You have successfully logged out!')
                    break
        else:
            print('Wrong card number or PIN!')
            logged_in_user = None
    choice = UI.main_menu()
print('Bye!')

db.close()

