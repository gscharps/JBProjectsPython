import sqlite3
import random

#set up db
class Database:
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
    def acct_exists(self, Account):
        #don't forget to commit after query
        pass
    def insert_acct(self, Account):
        #don't forget to commit after query
        pass
    def get_balance(self, acct_num, pin):
        #need to commit somewhere
        return cur.execute('SELECT balance FROM card WHERE pin=? AND number=?', pin, acct_num)
    def close(self):
        conn.close()


class Account:
    def __init__(self, id, number, pin, balance):
        self.id = id
        self.number = number
        self.pin = pin
        self.balance = balance
class AccountGenerator:
    acct_num_generator = 10000000
    id_generator = 0
    def CreateAccount(self):
        #use random generator to create
        #account numbers until one is found that is not in database

        #returns an Account object
        pass
    def check_sum(cardNumNoCheckSum):
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
    def main_menu():
        print('\n1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        return int(input())
    def logged_in_menu():
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')
        return int(input())
    def login(acct_num, pin):
        retVal = False
        all_acct_nums = database.keys()
        if acct_num in all_acct_nums:
            test_pin = database[acct_num]['pin']
            if pin == test_pin:
                retVal = True
            else:
                retVal = False
        return retVal
    def display_card_info(Acct):
        print('You card has been created')
        print('Your card number:')
        #cardNumNoCheckSum = 400000000000000 + Account.acct_num
        print(Acct.number)
        #cardNumWithCheckSum = cardNumNoCheckSum*10 + check_sum(str(cardNumNoCheckSum))
        #print(str(cardNumWithCheckSum))
        print('Your card PIN:') 
        print(Acct.pin)
        #cur.execute('SELECT pin FROM card WHERE number=:num', {"num": Account.acct_num})
        #print(cur.fetchone())

UI = UserInterface()
db = Database()
choice = UI.main_menu()

while choice != 0:
    if choice == 1:
        newAcct = AccountGenerator.CreateAccount()
        Database.insert_acct(newAcct)
        UI.display_card_info(newAcct)
        continue
        #if Database.acct_exists(newAcct):
        #    print('Account already exists')
        #    choice = main_menu()
        #    continue
        #else:
        #    Database.insert_acct(newAcct)
        #    print('\nYour card has been created')
        #    display_card_info(newAcct)
        #    acct_num_generator += 1
        #    id_generator += 1
    elif choice == 2:
        number = int(input('\nEnter your card number:'))
        pin = int(input('Enter your PIN:'))
        if login(acct_num, pin):
            print('\nYou have successfully logged in!')
            logged_in_choice = logged_in_menu()
            while logged_in_choice == 1:
                print('Balance: ' + str(get_balance(acct_num, pin)))
                logged_in_choice = logged_in_menu()
            if logged_in_choice == 2:
                choice = main_menu()
                continue
            else:
                break
        else:
            print('Wrong card number or PIN!')
            logged_in_user = None
    choice = main_menu()
print('Bye!')

db.close()

