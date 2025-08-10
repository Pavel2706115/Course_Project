from personal_finance_tracker import TransactionManager, Transaction

def main_menu():
    manager = TransactionManager()
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            add_transaction_ui(manager)
        elif choice == "2":
            view_transactions_ui(manager)
        elif choice == "3":
            edit_transaction_ui(manager)
        elif choice == "4":
            delete_transaction_ui(manager)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

def add_transaction_ui(manager):
    try:
        amount = float(input("Amount: "))
        date = input("Date (YYYY-MM-DD): ")
        category = input("Category: ")
        payment_method = input("Payment Method: ")
        tags = input("Tags (comma separated): ").split(",") if input("Any tags? (y/n): ").lower() == "y" else []
        tags = [tag.strip() for tag in tags if tag.strip()]
        transaction = Transaction(amount, date, category, payment_method, tags)
        manager.add_transaction(transaction.to_dict())
        print("Transaction added successfully.")
    except ValueError:
        print("Invalid input. Please enter the correct data types.")

def view_transactions_ui(manager):
    transactions = manager.view_transactions()
    if not transactions:
        print("No transactions found.")
        return
    for i, t in enumerate(transactions):
        print(f"\nTransaction {i+1}")
        print(f"  Amount: {t['amount']:.2f}")
        print(f"  Date: {t['date']}")
        print(f"  Category: {t['category']}")
        print(f"  Payment Method: {t['payment_method']}")
        print(f"  Tags: {', '.join(t['tags']) if t['tags'] else 'None'}")
        print("-" * 30)

def edit_transaction_ui(manager):
    try:
        index = int(input("Enter transaction number to edit: ")) - 1
        transactions = manager.view_transactions()
        if not (0 <= index < len(transactions)):
            print("Invalid transaction number.")
            return
        print("Enter new values (leave blank to keep current):")
        t = transactions[index]
        amount = input(f"Amount [{t['amount']}]: ") or t['amount']
        date = input(f"Date [{t['date']}]: ") or t['date']
        category = input(f"Category [{t['category']}]: ") or t['category']
        payment_method = input(f"Payment Method [{t['payment_method']}]: ") or t['payment_method']
        tags = input(f"Tags (comma separated) [{', '.join(t['tags'])}]: ") or ','.join(t['tags'])
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
        updated_transaction = Transaction(float(amount), date, category, payment_method, tags)
        manager.edit_transaction(index, updated_transaction.to_dict())
        print("Transaction updated.")
    except (ValueError, IndexError):
        print("Invalid input or transaction number.")

def delete_transaction_ui(manager):
    try:
        index = int(input("Enter transaction number to delete: ")) - 1
        manager.delete_transaction(index)
        print("Transaction deleted.")
    except (ValueError, IndexError):
        print("Invalid transaction number.")

if __name__ == "__main__":
    main_menu()