# Write your code here
import sqlite3

database = {}

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

acct_num_generator = 10000000

choice = main_menu()
logged_in_user = None
while choice != 0:
    if choice == 1:
        database[acct_num_generator] = {"pin" : 1000, "balance": 0}
        print('\nYour card has been created')
        print('Your card number:')
        cardNumNoCheckSum = 400000000000000 + acct_num_generator
        cardNumWithCheckSum = cardNumNoCheckSum*10 + check_sum(str(cardNumNoCheckSum))
        print(str(cardNumWithCheckSum))
        print('Your card PIN:')
        print(str(database[acct_num_generator]['pin']))
        acct_num_generator += 1
    elif choice == 2:
        acct_num = int(input('\nEnter your card number:')[6:15])
        pin = int(input('Enter your PIN:'))
        if login(acct_num, pin):
            print('\nYou have successfully logged in!')
            logged_in_user = acct_num
            logged_in_choice = logged_in_menu()
            while logged_in_choice == 1:
                print('Balance: ' + str(database[logged_in_user]['balance']))
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
