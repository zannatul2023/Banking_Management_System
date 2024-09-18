import json
import os
import logging
from datetime import datetime, timedelta

# Logger setup
logging.basicConfig(filename='banking_system.log', level=logging.INFO)

# File handling class
class FileHandler:
    @staticmethod
    def save_to_file(data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_from_file(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return {}

# Authentication Class
class Authentication:
    @staticmethod
    def signup(accounts, account_number, name, password, account_type):
        if account_number in accounts:
            print("Account already exists!")
            return False
        accounts[account_number] = {
            "name": name,
            "password": password,
            "account_type": account_type,
            "balance": 0,
            "transactions": [],
            "last_withdrawal": None,
            "withdrawal_today": 0
        }
        print(f"Account created successfully for {name}!")
        logging.info(f"Account created for {name} ({account_number})")
        return True

    @staticmethod
    def login(accounts, account_number, password):
        account = accounts.get(account_number)
        if account and account["password"] == password:
            print(f"Welcome back, {account['name']}!")
            logging.info(f"{account['name']} ({account_number}) logged in")
            return account_number
        print("Invalid account number or password!")
        return None

# Account Class
class Account:
    def __init__(self, account_number, accounts):
        self.account_number = account_number
        self.accounts = accounts
        self.account = self.accounts[account_number]

    def deposit(self, amount):
        self.account['balance'] += amount
        self.account['transactions'].append(f"Deposit: {amount} on {datetime.now()}")
        print(f"{amount} deposited. New balance: {self.account['balance']}")
        logging.info(f"{amount} deposited to {self.account_number}")
        return self.account['balance']

    def withdraw(self, amount):
        if self._can_withdraw(amount):
            self.account['balance'] -= amount
            self.account['transactions'].append(f"Withdraw: {amount} on {datetime.now()}")
            print(f"{amount} withdrawn. New balance: {self.account['balance']}")
            logging.info(f"{amount} withdrawn from {self.account_number}")
            self._update_withdrawal_limit(amount)
            return self.account['balance']
        else:
            print("Withdrawal denied: Insufficient funds or withdrawal limit reached.")
            return None

    def check_balance(self):
        print(f"Your current balance is: {self.account['balance']}")
        return self.account['balance']

    def show_transaction_history(self):
        print(f"Transaction history for {self.account['name']}:")
        for transaction in self.account['transactions']:
            print(transaction)

    def _can_withdraw(self, amount):
        # Check for savings account withdrawal limit (e.g., $1000/day)
        if self.account['account_type'] == "Savings":
            if self.account['withdrawal_today'] + amount > 1000:
                print("Withdrawal limit for today reached.")
                return False
        return self.account['balance'] >= amount

    def _update_withdrawal_limit(self, amount):
        if self.account['last_withdrawal']:
            if datetime.now().date() != datetime.strptime(self.account['last_withdrawal'], '%Y-%m-%d').date():
                self.account['withdrawal_today'] = 0
        self.account['withdrawal_today'] += amount
        self.account['last_withdrawal'] = str(datetime.now().date())

# Admin Class
class Admin:
    def __init__(self, admin_password):
        self.admin_password = admin_password

    def login(self, password):
        if password == self.admin_password:
            print("Admin logged in successfully!")
            logging.info("Admin logged in")
            return True
        print("Invalid admin password!")
        return False

    def view_all_accounts(self, accounts):
        print("All Accounts:")
        for acc_num, account in accounts.items():
            print(f"Account Number: {acc_num}, Name: {account['name']}, Balance: {account['balance']}")

    def view_transaction_history(self, accounts, account_number):
        if account_number in accounts:
            account = accounts[account_number]
            print(f"Transaction history for {account['name']}:")
            for transaction in account['transactions']:
                print(transaction)
        else:
            print("Account not found!")

# Main Bank Management System
class BankSystem:
    def __init__(self):
        self.accounts = FileHandler.load_from_file('accounts.json')
        self.admin_password = "admin123"
        self.admin = Admin(self.admin_password)

    def start(self):
        while True:
            print("\n1. Sign Up\n2. Login\n3. Admin Login\n4. Exit")
            choice = input("Select an option: ")
            if choice == '1':
                self.signup()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.admin_login()
            elif choice == '4':
                FileHandler.save_to_file(self.accounts, 'accounts.json')
                print("Exiting system.")
                break
            else:
                print("Invalid choice!")

    def signup(self):
        account_number = input("Enter Account Number: ")
        name = input("Enter your name: ")
        password = input("Enter a password: ")
        account_type = input("Enter account type (Savings/Current): ")
        Authentication.signup(self.accounts, account_number, name, password, account_type)

    def login(self):
        account_number = input("Enter Account Number: ")
        password = input("Enter your password: ")
        account_id = Authentication.login(self.accounts, account_number, password)
        if account_id:
            self.user_menu(account_id)

    def user_menu(self, account_number):
        account = Account(account_number, self.accounts)
        while True:
            print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transaction History\n5. Logout")
            choice = input("Select an option: ")
            if choice == '1':
                amount = float(input("Enter amount to deposit: "))
                account.deposit(amount)
            elif choice == '2':
                amount = float(input("Enter amount to withdraw: "))
                account.withdraw(amount)
            elif choice == '3':
                account.check_balance()
            elif choice == '4':
                account.show_transaction_history()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    def admin_login(self):
        password = input("Enter Admin Password: ")
        if self.admin.login(password):
            self.admin_menu()

    def admin_menu(self):
        while True:
            print("\n1. View All Accounts\n2. View Transaction History\n3. Logout")
            choice = input("Select an option: ")
            if choice == '1':
                self.admin.view_all_accounts(self.accounts)
            elif choice == '2':
                account_number = input("Enter Account Number to view transactions: ")
                self.admin.view_transaction_history(self.accounts, account_number)
            elif choice == '3':
                break
            else:
                print("Invalid choice!")

# Run the Bank System
if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.start()
