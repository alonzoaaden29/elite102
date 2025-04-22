import sqlite3
import hashlib
import tkinter 

DATABASE_NAME = 'bank.db'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
    return conn

def hash_pin(pin):
    hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
    return hashed_pin

def verify_pin(entered_pin, stored_hash):
    return hash_pin(entered_pin) == stored_hash

def create_account():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            name = input("Enter account holder name: ")
            pin = input("Enter a 4-digit PIN for your account: ")
            if not pin.isdigit() or len(pin) != 4:
                print("Invalid PIN. PIN must be a 4-digit number.")
                return

            initial_deposit = input("Enter initial deposit amount (minimum 0.0): ")
            try:
                balance = float(initial_deposit)
                if balance < 0:
                    print("Initial deposit cannot be negative.")
                    return
            except ValueError:
                print("Invalid deposit amount.")
                return

            hashed_pin = hash_pin(pin)
            cursor.execute("INSERT INTO accounts (name, pin, balance) VALUES (?, ?, ?)", (name, hashed_pin, balance))
            conn.commit()
            account_number = cursor.lastrowid
            print(f"Account created successfully! Your account number is: {account_number}")
        except sqlite3.Error as e:
            print(f"Error creating account: {e}")
            conn.rollback()
        finally:
            conn.close()

def login():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            account_number_input = input("Enter your account number: ")
            pin_input = input("Enter your PIN: ")

            cursor.execute("SELECT account_number, pin, name FROM accounts WHERE account_number = ?", (account_number_input,))
            account = cursor.fetchone()

            if account and verify_pin(pin_input, account[1]):
                print(f"\nWelcome, {account[2]} (Account #{account[0]})!")
                return account[0]
            else:
                print("Invalid account number or PIN. Login failed.")
                return None
        except sqlite3.Error as e:
            print(f"Error during login: {e}")
        finally:
            conn.close()
    return None

def main():

    while True:
        print("\n--- Online Banking System ---")
        print("1. Login to Existing Account")
        print("2. Create New Account")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            logged_in_account = login()
            if logged_in_account:
                while True:
                    print("\n--- Account Menu ---")
                    print("1. Logout")
                    account_action = input("Enter your choice: ")

                    if account_action == '1':
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")

        elif choice == '2':
            create_account()

        elif choice == '3':
            print("Thank you for using our online banking system!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

#add withdraw, check balance, and deposit

