import sqlite3
import random


def connection():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    return conn, cur


def create_table():
    conn, cur = connection()
    cur.execute("""CREATE TABLE IF NOT EXISTS card(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            pin TEXT,
            balance INTEGER)
        """)
    conn.commit()
    cur.close()


def cards_data_base(new_card, pin, starting_balance=0):
    conn, cur = connection()
    data = new_card, pin, starting_balance
    insert_stm = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)"
    cur.execute(insert_stm, data)
    conn.commit()
    cur.close()


def luhn_alg_verification(new_card):
    to_be_verified = list(str(new_card))
    last_digit = to_be_verified[-1]
    to_be_verified = to_be_verified[0:15]
    verified_card = []
    checksum = 0
    for index, number in enumerate(to_be_verified):
        if index == 0 or index % 2 == 0:
            x = int(number) * 2
            verified_card.append(x)
        else:
            verified_card.append(int(number))
    for index, number in enumerate(verified_card):
        if number > 9:
            verified_card[index] = number - 9
    control_number = sum(verified_card)
    for i in range(1, 11):
        if (control_number + i) % 10 == 0:
            checksum = i
        else:
            i += 1
    if checksum == int(last_digit):
        return True
    else:
        return False


def new_account():
    first_digits = 400000
    account_number = random.randint(1000000000, 9999999999)
    new_card = int((str(first_digits) + str(account_number)))
    pin = random.randint(1000, 9999)
    if luhn_alg_verification(new_card):
        return new_card, pin
    else:
        return new_account()


def log_in():
    conn, cur = connection()
    card_verification = int(input('\nEnter your card number:\n'))
    pin_verification = int(input('Enter your PIN:\n'))
    select_stm = "SELECT number, pin, balance FROM card"
    cur.execute(select_stm)
    data = cur.fetchall()
    for row in data:
        if card_verification == int(row[0]) and pin_verification == int(row[1]):
            print("You have successfully logged in!\n")
            balance(row)
        else:
            continue
    print('\nWrong card number or PIN!\n')
    menu()


def balance(row):
    total_income = row[2]
    while True:
        conn, cur = connection()
        print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
        action = input()
        card_number = row[0]
        balance_from_sql = cur.execute("SELECT balance FROM card WHERE number=?", (card_number,))
        if action == '1':
            for value in balance_from_sql:
                print(f'\nBalance: {value[0]}\n')
        elif action == '2':
            add_income = input("\nEnter income:\n")
            print("Income was added!\n")
            total_income += int(add_income)
            update_stm = "UPDATE card SET balance = ? WHERE number = ?"
            cur.execute(update_stm, (total_income, card_number))
            conn.commit()
        elif action == '3':
            cur.close()
            transfer(card_number)
        elif action == '4':
            cur.close()
            close_account(row)
            print('\nThe account has been closed!\n')
            menu()
        elif action == '5':
            cur.close()
            menu()
        else:
            print("\nBye!")
            quit()


def close_account(row):
    conn, cur = connection()
    delete_by_number = row[0]
    delete_stm = "DELETE FROM card WHERE number=?"
    cur.execute(delete_stm, (delete_by_number,))
    conn.commit()


def transfer(card_number):
    conn, cur = connection()
    number_for_transfer = input("\nTransfer\nEnter card number: \n")
    if not luhn_alg_verification(number_for_transfer):
        print('Probably you made a mistake in the card number. Please try again!\n')
    else:
        select_stm_cards = "SELECT number FROM card"
        cur.execute(select_stm_cards)
        all_cards = cur.fetchall()
        all_cards_list = [card[0] for card in all_cards]
        if number_for_transfer not in all_cards_list:
            print('Such a card does not exist.\n')
        else:
            transfer_money = int(input("Enter how much money you want to transfer:"))
            select_stm_balance = "SELECT balance FROM card where number=?"
            cur.execute(select_stm_balance, (card_number,))
            balance_first_card = cur.fetchall()
            for el in balance_first_card:
                if int(transfer_money) > int(el[0]):
                    print('Not enough money!\n')
                else:
                    x = el[0]
                    cur.execute(select_stm_balance, (number_for_transfer,))
                    balance_second_card = cur.fetchall()
                    for el_2 in balance_second_card:
                        y = el_2[0]
                    removed_from_first_card = x - transfer_money
                    added_to_second_card = y + transfer_money
                    update_balance_stm = "UPDATE card SET balance=? WHERE number=?"
                    cur.execute(update_balance_stm, (removed_from_first_card, card_number))
                    cur.execute(update_balance_stm, (added_to_second_card, number_for_transfer))
                    conn.commit()
                    print("Success!\n")


def choice():
    print("""1. Create an account
2. Log into account
0. Exit""")
    action = input()
    return action


def menu():
    create_table()
    action = choice()
    if action == '1':
        new_card, pin = new_account()
        print("\nYour card has been created")
        print(f'Your card number:\n{new_card}')
        print(f'Your card PIN:\n{pin}\n')
        cards_data_base(new_card, pin)
        menu()
    if action == '2':
        log_in()
    if action == '0':
        print("\nBye!")
        quit()


menu()
