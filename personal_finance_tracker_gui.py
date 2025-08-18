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

        self.create_add_transaction_frame()
        self.create_view_transactions_frame()

        self.notebook.add(self.add_frame, text="Add Transaction")
        self.notebook.add(self.view_frame, text="View Transactions")
        self.notebook.pack(fill="both", expand=True)

        # Update transactions when switching to the view tab
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
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

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            date = self.date_entry.get()
            category = self.category_entry.get()
            payment_method = self.payment_method_entry.get()
            tags = self.tags_entry.get().split(",")
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

    