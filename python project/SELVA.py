import sqlite3
from datetime import datetime

# Database initialization
conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL
    )
''')
conn.commit()

# Function to add an expense
def add_expense(date, category, amount):
    cursor.execute('INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)', (date, category, amount))
    conn.commit()

# Function to view expenses
def view_expenses():
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses recorded.")
    else:
        print("Expense History:")
        print("{:<5} {:<15} {:<15} {:<10}".format("ID", "Date", "Category", "Amount"))
        print("="*45)
        for expense in expenses:
            print("{:<5} {:<15} {:<15} ${:<10.2f}".format(*expense))

# Function to get total expenses for a category or date range
def get_total_expenses(category=None, start_date=None, end_date=None):
    query = 'SELECT SUM(amount) FROM expenses'
    conditions = []

    if category:
        conditions.append(f'category="{category}"')
    if start_date:
        conditions.append(f'date >= "{start_date}"')
    if end_date:
        conditions.append(f'date <= "{end_date}"')

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query)
    total_expense = cursor.fetchone()[0]

    return total_expense if total_expense else 0.0

# User interface
while True:
    print("\nExpense Tracker Menu:")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Get Total Expenses")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        date = input("Enter the date (YYYY-MM-DD): ")
        category = input("Enter the category: ")
        amount = float(input("Enter the amount: $"))
        add_expense(date, category, amount)
        print("Expense added successfully!")

    elif choice == '2':
        view_expenses()

    elif choice == '3':
        category = input("Enter the category (press Enter for all categories): ")
        start_date = input("Enter the start date (press Enter for no start date): ")
        end_date = input("Enter the end date (press Enter for no end date): ")

        total_expense = get_total_expenses(category, start_date, end_date)
        print(f"Total Expenses: ${total_expense:.2f}")

    elif choice == '4':
        print("Exiting Expense Tracker. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
