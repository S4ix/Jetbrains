import secrets
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()

def checksum_gen(number):
    all_numbers = 0
    for i in range(15):
        digit = int(number[i])
        if not i % 2:
            digit *= 2
            if digit > 9:
                digit -= 9
        all_numbers += digit
    if all_numbers % 10:
        checksum = 10 - (all_numbers % 10)
    else:
        checksum = 0
    return checksum


def transfer(own_account_number):
    destination = input('Transfer\nEnter card number:')
    if destination != own_account_number:
        last_digit_destination = destination[-1]
        destination_without_checksum = destination[:-1]
        if str(checksum_gen(destination_without_checksum)) == last_digit_destination:
            cur.execute(f'SELECT COUNT(*) FROM card WHERE number={destination}')
            if cur.fetchone()[0]:
                cur.execute(f'SELECT balance FROM card WHERE number={own_account_number}')
                balance = cur.fetchone()[0]
                transfer_money = int(input('Enter how much money you want to transfer:'))
                if balance < transfer_money:
                    print(f'Not enough money!')
                else:
                    cur.execute(f'UPDATE card SET balance = balance - {transfer_money} WHERE number={own_account_number}')
                    cur.execute(f'UPDATE card SET balance = balance + {transfer_money} WHERE number={destination}')
                    conn.commit()
                    print('Success!')
            else:
                print('Such a card does not exist.')
        else:
            print('Probably you made a mistake in the card number. Please try again!')
    else:
        print("You can't transfer money to the same account!")

class Account:
    def __init__(self):
        self.pin = '%04d' % secrets.randbelow(10000)
        self.number = 0
        cur.execute(f'INSERT into card VALUES (NULL, {self.number}, {self.pin}, 0)')
        conn.commit()
        cur.execute(f'SELECT id FROM card WHERE pin={self.pin} AND number=0')
        account_id = cur.fetchone()[0]
        account_number = '%09d' % account_id
        checksum = checksum_gen('400000' + account_number)
        self.number = "400000" + account_number + str(checksum)
        self.balance = 0
        cur.execute(f'UPDATE card SET number = {self.number} WHERE id={account_id}')
        conn.commit()
        print('Your card has been created')
        print(f'Your card number:\n{self.number}')
        print(f'Your card PIN:\n{self.pin}\n')


selection = 3
while selection != 0:
    logged_in = False
    selection = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    if selection == 1:
        account = Account()
    elif selection == 2:
        number = input('Enter your card number:\n')
        cur.execute(f'SELECT number, pin, balance FROM card WHERE number={number}')
        result = cur.fetchone()
        if result:
            selected_account_number = result[0]
            selected_account_pin = result[1]
            selected_account_balance = result[2]

            if selected_account_number == number:
                pin = input('Enter your PIN:\n')
                if pin == selected_account_pin:
                    print('You have successfully logged in!\n')
                    logged_in = True
                else:
                    print('Wrong card number or PIN!\n')
                    logged_in = False
        else:
            print('Wrong card number or PIN!')
        while logged_in:
            transaction = int(input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit"))
            if transaction == 1:
                cur.execute(f'SELECT balance FROM card WHERE number={selected_account_number}')
                print(f'Balance: {cur.fetchone()[0]}\n')
            if transaction == 2:
                income = int(input('Enter income:'))
                cur.execute(f'UPDATE card SET balance = balance + {income} WHERE number={selected_account_number}')
                conn.commit()
                print('Income was added!')
            if transaction == 3:
                transfer(selected_account_number)
            if transaction == 4:
                cur.execute(f'DELETE FROM card WHERE number = {selected_account_number}')
                conn.commit()
                print('The account has been closed!')
            if transaction == 5:
                logged_in = False
                print('You have successfully logged out!\n')
            if transaction == 0:
                logged_in = False
                selected_account_number = '0'
                selected_account_pin = '0'
                selected_account_balance = 0
                selection = 0
                print('Bye!')
    elif selection == 0:
        print('Bye!')

