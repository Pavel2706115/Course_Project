import tkinter as tk
from tkinter import messagebox
from personal_finance_tracker import TransactionManager, Transaction

def add_transaction():
    # Example: get data from entry fields and add transaction
    try:
        amount = float(amount_entry.get())
        date = date_entry.get()
        category = category_entry.get()
        payment_method = payment_method_entry.get()
        tags = tags_entry.get().split(",")
        transaction = Transaction(amount, date, category, payment_method, tags)
        manager.add_transaction(transaction.to_dict())
        messagebox.showinfo("Success", "Transaction added!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

manager = TransactionManager()

root = tk.Tk()
root.title("Personal Finance Tracker")

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Category:").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Payment Method:").pack()
payment_method_entry = tk.Entry(root)
payment_method_entry.pack()

tk.Label(root, text="Tags (comma separated):").pack()
tags_entry = tk.Entry(root)
tags_entry.pack()

tk.Button(root, text="Add Transaction", command=add_transaction).pack()

root.mainloop()