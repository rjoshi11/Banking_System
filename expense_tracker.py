from datetime import date, datetime
import matplotlib.pyplot as plt
def add_expense():
    while True:
        categ=input("Enter category (e.g., Food, Travel): ")
        amount=float(input("Enter amount:"))
        print(f"Date: {date.today()}")

        with open("expenses.txt", "a") as f:
            f.write(f"category: {categ},amount: {amount},Date: {date.today()}\n")
        print("Expense added successfully!")
        # (Expense recorded in expenses.txt)
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
  Calculates and displays the monthly summary of expenses, including a pie chart.
  """

  current_month = date.today().month
  current_year = date.today().year
  total_expenses = 0
  category_expenses = {}

  try:
    with open("expenses.txt", "r") as f:
      for line in f:
        parts = line.strip().split(",")
        if len(parts) >= 3:  # Ensure enough parts for category and date
          category = parts[0].split(": ")[1]
          amount = float(parts[1].split(": ")[1])
          expense_date = datetime.strptime(parts[2].split(": ")[1], "%Y-%m-%d").date()

          if expense_date.month == current_month and expense_date.year == current_year:
            total_expenses += amount
            category_expenses[category] = category_expenses.get(category, 0) + amount

  except FileNotFoundError:
    print("Expense tracker file not found. No summary available.")
    return

  # Print Monthly Summary
  print(f"Monthly Summary (December {current_year}):")
  print(f"Total Expenses: ${total_expenses:.2f}")
  print("By Category:")

  for category, amount in category_expenses.items():
    print(f"{category}: ${amount:.2f}")

  # Create Pie Chart Data
  labels = list(category_expenses.keys())
  sizes = list(category_expenses.values())

  # Create Pie Chart
  fig, ax = plt.subplots()
  ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
  ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  ax.set_title(f"Monthly Expenses ({current_month}/{current_year})")
  plt.show()

