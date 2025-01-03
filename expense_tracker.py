from datetime import date, datetime
import matplotlib.pyplot as plt

# Global variable for budget
BUDGET_LIMIT = 0

def set_budget_alert():
    """
    Sets a monthly budget limit and displays a warning if spending approaches or exceeds the limit.
    """
    global BUDGET_LIMIT
    BUDGET_LIMIT = float(input("Set your monthly spending limit: "))
    print(f"Budget limit set to ${BUDGET_LIMIT:.2f}.")

def add_expense():
    """
    Adds an expense to the tracker and checks against the monthly budget limit.
    """
    global BUDGET_LIMIT
    while True:
        categ = input("Enter category (e.g., Food, Travel): ")
        amount = float(input("Enter amount: "))
        print(f"Date: {date.today()}")

        with open("expenses.txt", "a") as f:
            f.write(f"category: {categ},amount: {amount},Date: {date.today()}\n")
        print("Expense added successfully!")

        # Check if the budget is exceeded
        current_month = date.today().month
        current_year = date.today().year
        total_monthly_expenses = 0

        with open("expenses.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    amount = float(parts[1].split(": ")[1])
                    expense_date = datetime.strptime(parts[2].split(": ")[1], "%Y-%m-%d").date()
                    if expense_date.month == current_month and expense_date.year == current_year:
                        total_monthly_expenses += amount

        if BUDGET_LIMIT > 0:
            if total_monthly_expenses > BUDGET_LIMIT:
                print(f"⚠️ Warning: You have exceeded your monthly budget of ${BUDGET_LIMIT:.2f}!")
            elif total_monthly_expenses > 0.9 * BUDGET_LIMIT:
                print(f"⚠️ Alert: You are close to your monthly budget limit! Spent: ${total_monthly_expenses:.2f}")

        break

def view_expenses():
    """
    Reads and displays all expenses from the expense tracker file, grouped by category.
    """
    try:
        with open("expenses.txt", "r") as f:
            expenses = f.readlines()
            if not expenses:
                print("No expenses recorded yet.")
                return

            print("Expenses:")
            categories = {}
            for expense in expenses:
                details = expense.strip().split(",")
                category = details[0].split(": ")[1]
                if category not in categories:
                    categories[category] = []
                categories[category].append(expense.strip())

            for category, expenses in categories.items():
                print(f"\n{category}:")
                if not expenses:
                    print("No expenses recorded.")
                else:
                    for expense in expenses:
                        print(f"- {expense}")

    except FileNotFoundError:
        print("Expense tracker file not found. No expenses to display.")

def monthly_summary():
    """
    Calculates and displays the monthly and yearly summaries of expenses, including pie charts.
    """
    current_month = date.today().month
    current_year = date.today().year
    total_monthly_expenses = 0
    total_yearly_expenses = 0
    monthly_expenses = {}
    yearly_expenses = {}

    try:
        with open("expenses.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    category = parts[0].split(": ")[1]
                    amount = float(parts[1].split(": ")[1])
                    expense_date = datetime.strptime(parts[2].split(": ")[1], "%Y-%m-%d").date()

                    # Monthly Expenses
                    if expense_date.month == current_month and expense_date.year == current_year:
                        total_monthly_expenses += amount
                        monthly_expenses[category] = monthly_expenses.get(category, 0) + amount

                    # Yearly Expenses
                    if expense_date.year == current_year:
                        total_yearly_expenses += amount
                        yearly_expenses[category] = yearly_expenses.get(category, 0) + amount

    except FileNotFoundError:
        print("Expense tracker file not found. No summary available.")
        return

    # Print Summaries
    print(f"Monthly Summary ({current_month}/{current_year}):")
    print(f"Total Monthly Expenses: ${total_monthly_expenses:.2f}")
    for category, amount in monthly_expenses.items():
        print(f"{category}: ${amount:.2f}")

    print(f"\nYearly Summary ({current_year}):")
    print(f"Total Yearly Expenses: ${total_yearly_expenses:.2f}")
    for category, amount in yearly_expenses.items():
        print(f"{category}: ${amount:.2f}")

    # Generate Pie Charts
    if monthly_expenses:
        plt.figure(figsize=(10, 5))
        plt.pie(monthly_expenses.values(), labels=monthly_expenses.keys(), autopct='%1.1f%%', startangle=90)
        plt.title(f"Monthly Expenses ({current_month}/{current_year})")
        plt.axis('equal')
        plt.show()

    if yearly_expenses:
        plt.figure(figsize=(10, 5))
        plt.pie(yearly_expenses.values(), labels=yearly_expenses.keys(), autopct='%1.1f%%', startangle=90)
        plt.title(f"Yearly Expenses ({current_year})")
        plt.axis('equal')
        plt.show()
