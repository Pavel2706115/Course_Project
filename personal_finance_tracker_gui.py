import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from personal_finance_tracker import TransactionManager, Transaction

class FinanceTrackerApp(tk.Tk):
    def __init__(self, manager):
        super().__init__()
        self.title("Personal Finance Tracker")
        self.manager = manager

        self.notebook = ttk.Notebook(self)
        self.add_frame = tk.Frame(self.notebook)
        self.view_frame = tk.Frame(self.notebook)
        self.edit_frame = tk.Frame(self.notebook)
        self.delete_frame = tk.Frame(self.notebook)

        self.create_add_transaction_frame()
        self.create_view_transactions_frame()
        self.create_edit_transaction_frame()
        self.create_delete_transaction_frame()

        self.notebook.add(self.add_frame, text="Add Transaction")
        self.notebook.add(self.view_frame, text="View Transactions")
        self.notebook.add(self.edit_frame, text="Edit Transaction")
        self.notebook.add(self.delete_frame, text="Delete Transaction")
        self.notebook.pack(fill="both", expand=True)

        # Update transactions when switching to the view tab
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, _):
        if self.notebook.index(self.notebook.select()) == 1:
            self.update_transactions()

    def create_add_transaction_frame(self):
        frame = self.add_frame
        tk.Label(frame, text="Amount:").pack()
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.pack()

        tk.Label(frame, text="Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(frame)
        self.date_entry.pack()

        tk.Label(frame, text="Category:").pack()
        self.category_entry = tk.Entry(frame)
        self.category_entry.pack()

        tk.Label(frame, text="Payment Method:").pack()
        self.payment_method_entry = tk.Entry(frame)
        self.payment_method_entry.pack()

        tk.Label(frame, text="Tags (comma separated):").pack()
        self.tags_entry = tk.Entry(frame)
        self.tags_entry.pack()

        tk.Button(frame, text="Add Transaction", command=self.add_transaction).pack(pady=5)

    def create_view_transactions_frame(self):
        frame = self.view_frame
        self.transactions_text = tk.Text(frame, width=50, height=15, state='disabled')
        self.transactions_text.pack()
    
    def create_edit_transaction_frame(self):
        frame = self.edit_frame
        tk.Label(frame, text="Enter transaction number to edit:").pack()
        self.edit_index_entry = tk.Entry(frame)
        self.edit_index_entry.pack()
        tk.Button(frame, text="Edit Transaction", command=self.edit_transaction).pack(pady=5)
    def create_delete_transaction_frame(self):
        frame = self.delete_frame
        tk.Label(frame, text="Enter transaction number to delete:").pack()
        self.delete_index_entry = tk.Entry(frame)
        self.delete_index_entry.pack()
        tk.Button(frame, text="Delete Transaction", command=self.delete_transaction).pack(pady=5)
        

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            date = self.date_entry.get()
            category = self.category_entry.get()
            payment_method = self.payment_method_entry.get()
            tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]
            transaction = Transaction(amount, date, category, payment_method, tags)
            self.manager.add_transaction(transaction.to_dict())
            messagebox.showinfo("Success", "Transaction added!")
            self.amount_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.payment_method_entry.delete(0, tk.END)
            self.tags_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_transaction(self):
        try:
            index = int(self.edit_index_entry.get()) - 1
            transactions = self.manager.view_transactions()
            if index < 0 or index >= len(transactions):
                messagebox.showerror("Error", "Invalid transaction number.")
                return
            t = transactions[index]
            # Pre-fill the add form with selected transaction
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, t['amount'])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, t['date'])
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, t['category'])
            self.payment_method_entry.delete(0, tk.END)
            self.payment_method_entry.insert(0, t['payment_method'])
            self.tags_entry.delete(0, tk.END)
            self.tags_entry.insert(0, ', '.join(t['tags']))
            # Remove the old transaction
            self.manager.delete_transaction(index)
            messagebox.showinfo("Info", "Edit the details in the Add Transaction tab and click 'Add Transaction' to save changes.")
            self.notebook.select(self.add_frame)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_transaction(self):
        try:
            index = int(self.delete_index_entry.get()) - 1
            transactions = self.manager.view_transactions()
            if index < 0 or index >= len(transactions):
                messagebox.showerror("Error", "Invalid transaction number.")
                return
            self.manager.delete_transaction(index)
            messagebox.showinfo("Success", "Transaction deleted!")
            self.delete_index_entry.delete(0, tk.END)
            self.update_transactions()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_transactions(self):
        try:
            transactions = self.manager.view_transactions()
            self.transactions_text.config(state='normal')
            self.transactions_text.delete(1.0, tk.END)
            if not transactions:
                self.transactions_text.insert(tk.END, "No transactions found.")
            else:
                for i, t in enumerate(transactions):
                    details = (
                        f"Transaction {i+1}:\n"
                        f"  Amount: {t['amount']}\n"
                        f"  Date: {t['date']}\n"
                        f"  Category: {t['category']}\n"
                        f"  Payment Method: {t['payment_method']}\n"
                        f"  Tags: {', '.join(t['tags']) if t['tags'] else 'None'}\n\n"
                    )
                    self.transactions_text.insert(tk.END, details)
            self.transactions_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    manager = TransactionManager()
    app = FinanceTrackerApp(manager)
    app.mainloop()