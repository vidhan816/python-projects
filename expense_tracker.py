import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

FILE_NAME = "expenses.csv"

# Create file if not exists
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(FILE_NAME, index=False)

# Function to add expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if date == "":
        date = datetime.today().strftime('%Y-%m-%d')

    category = input("Enter category (Food, Travel, Shopping, etc.): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    new_data = pd.DataFrame([[date, category, amount, description]],
                            columns=["Date", "Category", "Amount", "Description"])

    new_data.to_csv(FILE_NAME, mode='a', header=False, index=False)
    print("✅ Expense added successfully!")

# Function to view summary
def show_summary():
    df = pd.read_csv(FILE_NAME)
    print("\n📊 Expense Summary:")
    print(df.groupby("Category")["Amount"].sum())

# Function to visualize data
def visualize_data():
    df = pd.read_csv(FILE_NAME)
    df["Date"] = pd.to_datetime(df["Date"])

    # Monthly spending
    df["Month"] = df["Date"].dt.to_period("M")
    monthly = df.groupby("Month")["Amount"].sum()

    # Category spending
    category = df.groupby("Category")["Amount"].sum()

    # Plot Monthly Spending
    plt.figure()
    monthly.plot(kind='bar')
    plt.title("Monthly Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot Category Spending
    plt.figure()
    category.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Expenses by Category")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

# Main menu
def main():
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Visualize Data")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            show_summary()
        elif choice == '3':
            visualize_data()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()