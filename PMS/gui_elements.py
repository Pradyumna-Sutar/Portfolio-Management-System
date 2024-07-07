import tkinter as tk
from ttkbootstrap import Style, ttk

def create_label_entry(parent, text, row, master, dropdown=False):
    tk.Label(parent, text=text, bg=parent.cget("background")).grid(row=row, column=0, sticky='e', pady=5)
    if dropdown:
        transaction_type_var = tk.StringVar(master)
        transaction_type_var.set("Buy")
        transaction_type_dropdown = ttk.OptionMenu(parent, transaction_type_var, "Buy", "Sell")
        transaction_type_dropdown.grid(row=row, column=1, pady=5)
        return transaction_type_var
    else:
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, pady=5)
        return entry
