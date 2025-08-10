import json
import os

class TransactionManager:
    def __init__(self, filename='transactions.json'):
        self.filename = filename
        self.transactions = []
        self.load_transactions()

    def load_transactions(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.transactions = json.load(file)
        else:
            self.transactions = []

    def save_transactions(self):
        with open(self.filename, 'w') as file:
            json.dump(self.transactions, file, indent=4)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_transactions()

    def edit_transaction(self, index, updated_transaction):
        if 0 <= index < len(self.transactions):
            self.transactions[index] = updated_transaction
            self.save_transactions()
        else:
            raise IndexError("Transaction index out of range.")

    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            self.save_transactions()
        else:
            raise IndexError("Transaction index out of range.")

    def view_transactions(self):
        return self.transactions
    
class Transaction:
    def __init__(self, amount, date, category, payment_method, tags=None):
        self.amount = amount
        self.date = date
        self.category = category
        self.payment_method = payment_method
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            'amount': self.amount,
            'date': self.date,
            'category': self.category,
            'payment_method': self.payment_method,
            'tags': self.tags
        }
    
def print_transactions(transactions):
    if not transactions:
        print("No transactions found.")
        return
    for i, t in enumerate(transactions):
        print(f"Transaction {i+1}:")
        print(f"  Amount: {t['amount']}")
        print(f"  Date: {t['date']}")
        print(f"  Category: {t['category']}")
        print(f"  Payment Method: {t['payment_method']}")
        print(f"  Tags: {', '.join(t['tags']) if t['tags'] else 'None'}")
        print("-" * 30)

#Example usage:
if __name__ == "__main__":
    manager = TransactionManager()
    
    # Adding a transaction
    transaction = Transaction(100.0, '2023-10-01', 'Food', 'Credit Card', ['groceries'])
    manager.add_transaction(transaction.to_dict())
    
    # Viewing transactions
    print_transactions(manager.view_transactions())
    
    # Editing a transaction
    updated_transaction = Transaction(120.0, '2023-10-01', 'Food', 'Credit Card', ['groceries', 'snacks'])
    manager.edit_transaction(0, updated_transaction.to_dict())
    
    # Deleting a transaction
    manager.delete_transaction(0)
    
    # Viewing transactions after deletion
    print_transactions(manager.view_transactions())
# ...existing code...
