print("This is the personal finance tracker main module.")
from personal_finance_tracker_ui import TransactionManager, Transaction
# Initialize the transaction manager
transaction_manager = TransactionManager()
# Example usage of the transaction manager
def main():
    # Add a transaction
    transaction = Transaction(100.0, '2023-10-01', 'Food', 'Credit Card', ['groceries'])
    transaction_manager.add_transaction(transaction.to_dict())
    
    # View transactions
    print("Transactions:", transaction_manager.view_transactions())
    
    # Edit a transaction
    updated_transaction = Transaction(120.0, '2023-10-01', 'Food', 'Credit Card', ['groceries', 'snacks'])
    transaction_manager.edit_transaction(0, updated_transaction.to_dict())
    
    # Delete a transaction
    transaction_manager.delete_transaction(0)
    
    # View transactions after deletion
    print("Transactions after deletion:", transaction_manager.view_transactions())

# Define the TransactionManager and Transaction classes
# These classes handle the transactions and their management
