# Banking_Management_System
Banking Management System
Overview
The Banking Management System is a Python-based console application that allows users to create bank accounts, perform transactions (deposit and withdrawal), check balance, and view transaction history. It also includes an admin panel where the admin can view account details and transaction histories. This project is designed to provide a professional-level application for managing basic banking operations, with file-based persistence for long-term data storage.

Features
User Features:
Account Creation: Users can create an account by providing a unique account number, name, password, and selecting an account type (Savings/Current).
Deposit Money: Users can deposit money into their account.
Withdraw Money: Users can withdraw money from their account (Savings accounts have a daily withdrawal limit of $1000).
Check Balance: Users can check their account balance at any time.
Transaction History: Users can view a detailed list of all transactions made on their account.
Admin Features:
Admin Login: Admin can log into a secure admin panel using a password.
View All Accounts: Admin can view all registered accounts, along with the account balances.
Transaction History: Admin can view transaction history for any account by entering the account number.
Additional Features:
Daily Withdrawal Limits for Savings accounts ($1000/day).
Transaction Logging: All transactions (deposits, withdrawals) are logged for future reference.
File-based Storage: Account details and transaction histories are stored in a JSON file (accounts.json), ensuring persistent storage of data across sessions.
Activity Logs: Actions such as logins, deposits, and withdrawals are logged in a log file (banking_system.log).
