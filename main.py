#Account_file
#Main_menu
import datetime
import pwinput
import random
from colorama import Fore, Back, Style, init
from expense_tracker import set_budget_alert, add_expense, view_expenses, monthly_summary

# Initialize Colorama
init(autoreset=True)

def create_account():
    print(Fore.CYAN + "\n--- Create Account ---")
    name = input(Fore.YELLOW + "Enter your name: ")
    while True:
        try:
            deposit = float(input(Fore.YELLOW + "Enter your initial deposit (minimum 500): "))
            if deposit >= 500:
                break
            else:
                print(Fore.RED + "Initial deposit must be at least 500. Please try again.")
        except ValueError:
            print(Fore.RED + "Invalid deposit amount. Please enter a number.")
    acc_num = random.randrange(100000, 999999)
    print(Fore.GREEN + f"Your account number is {acc_num}")
    pswd = pwinput.pwinput(prompt=Fore.YELLOW + "Enter a password: ", mask="*")
    with open("accounts.txt", "a") as f:
        f.write(f"{name},{deposit},{acc_num},{pswd}\n")
    print(Fore.GREEN + "Account created successfully!")

def login():
    print(Fore.CYAN + "\n--- Login ---")
    try:
        with open("accounts.txt", "r") as f:
            user_id = float(input(Fore.YELLOW + "Enter your account number: "))
            password = pwinput.pwinput(prompt=Fore.YELLOW + "Enter your password: ", mask="*")
            accounts = f.readlines()

        for i, account in enumerate(accounts):
            details = account.strip().split(",")
            if len(details) == 4:
                name, deposit, stored_acc_num, stored_pswd = details
                if float(stored_acc_num) == user_id and stored_pswd == password:
                    print(Fore.GREEN + f"Login successful! Welcome, {name}.")
                    current_balance = float(deposit)

                    while True:
                        print(Fore.CYAN + "\n--- Banking Options ---")
                        print(Fore.YELLOW + "1. Deposit")
                        print(Fore.YELLOW + "2. Withdraw")
                        print(Fore.YELLOW + "3. Exit")
                        user_choice = int(input(Fore.CYAN + "Enter your choice: "))

                        if user_choice == 1:
                            # Deposit Logic
                            try:
                                deposit_amount = float(input(Fore.YELLOW + "Enter amount to deposit: "))
                                if deposit_amount > 0:
                                    current_balance += deposit_amount
                                    print(Fore.GREEN + f"Deposit successful! Current balance: {current_balance}")

                                    # Log transaction to transactions.txt

                                    with open("transactions.txt", "a") as t_file:
                                        t_file.write(f"Account: {user_id}, Deposit: {deposit_amount}, Balance: {current_balance} , Date:{datetime.date.today()}\n")
                                    print(Fore.GREEN + "(Transaction logged in transactions.txt)")

                                    # Update the accounts.txt file
                                    accounts[i] = f"{name},{current_balance},{stored_acc_num},{stored_pswd}\n"
                                    with open("accounts.txt", "w") as f:
                                        f.writelines(accounts)
                                else:
                                    print(Fore.RED + "Invalid deposit amount.")
                            except ValueError:
                                print(Fore.RED + "Invalid input. Please enter a numeric value.")

                        elif user_choice == 2:
                            # Withdraw Logic
                            try:
                                withdraw_amount = float(input(Fore.YELLOW + "Enter amount to withdraw: "))
                                if 0 < withdraw_amount <= current_balance:
                                    current_balance -= withdraw_amount
                                    print(Fore.GREEN + f"Withdrawal successful! Current balance: {current_balance}")

                                    # Log transaction to transactions.txt
                                    with open("transactions.txt", "a") as t_file:
                                        t_file.write(f"Account: {user_id}, Withdrawal: {withdraw_amount}, Balance: {current_balance}, Datetime:{datetime.date.today()}\n")
                                    print(Fore.GREEN + "(Transaction logged in transactions.txt)")

                                    # Update the accounts.txt file
                                    accounts[i] = f"{name},{current_balance},{stored_acc_num},{stored_pswd}\n"
                                    with open("accounts.txt", "w") as f:
                                        f.writelines(accounts)
                                elif withdraw_amount > current_balance:
                                    print(Fore.RED + "Insufficient balance.")
                                else:
                                    print(Fore.RED + "Invalid withdrawal amount.")
                            except ValueError:
                                print(Fore.RED + "Invalid input. Please enter a numeric value.")

                        elif user_choice == 3:
                            print(Fore.GREEN + "Thank you for banking with us. Goodbye!")
                            break

                        else:
                            print(Fore.RED + "Invalid choice. Please select a valid option.")

                    break
        else:
            print(Fore.RED + "Invalid account number or password.")
            return

    except FileNotFoundError:
        print(Fore.RED + "No accounts found. Please create an account first.")

# Main Menu (main.py)
while True:
    print(Back.BLUE + Fore.BLACK + "\n----------------------- Welcome to the Banking System! ------------------------")
    print(Fore.YELLOW + "1. Create Account")
    print(Fore.YELLOW + "2. Login")
    print(Fore.YELLOW + "3. Personal Expense Tracker")
    print(Fore.YELLOW + "4. Exit")
    choice = int(input(Fore.CYAN + "Enter your choice: "))
    if choice == 1:
        create_account()
    elif choice == 2:
        login()
    elif choice == 3:
        while True:
            print(
                Back.MAGENTA + Fore.WHITE + "\n------------------ Welcome To Your Personal Expense Tracker! ------------------")
            print(Fore.YELLOW + "1. Set Budget Alert")
            print(Fore.YELLOW + "2. Add Expense")
            print(Fore.YELLOW + "3. View Expenses")
            print(Fore.YELLOW + "4. Monthly Summary")
            print(Fore.YELLOW + "5. Back to Main Menu")
            tracker_choice = int(input(Fore.CYAN + "Enter your choice: "))

            if tracker_choice == 1:  # Fixed from "choice" to "tracker_choice"
                set_budget_alert()
            elif tracker_choice == 2:  # Fixed from "choice" to "tracker_choice"
                add_expense()
            elif tracker_choice == 3:  # Fixed from "choice" to "tracker_choice"
                view_expenses()
            elif tracker_choice == 4:  # Fixed from "choice" to "tracker_choice"
                monthly_summary()
            elif tracker_choice == 5:  # Fixed from "choice" to "tracker_choice"
                print(Fore.GREEN + "Returning to the main menu...")
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again.")
