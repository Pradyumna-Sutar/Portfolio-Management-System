import tkinter as tk
from tkinter import messagebox, simpledialog
from ttkbootstrap import Style
from ttkbootstrap import ttk  # Import ttk from ttkbootstrap
from pymongo import MongoClient
from PIL import Image, ImageTk  # Import PIL modules
from bson.objectid import ObjectId

# MongoDB connection parameters
MONGODB_URI = "mongodb+srv://romocromo90:romocromo9@cluster0.atmpzxm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "portfolio_tracker"

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Tooltip class
class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("Arial", 10))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = None

# Tkinter application
class PortfolioTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Portfolio Management")

        style = Style(theme='cosmo')
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TFrame", background=style.colors.bg)

        # Load and set background image
        self.background_image = Image.open("2.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(master, text="Welcome to Portfolio Management", font=("Arial", 18, "bold"), bg=style.colors.bg)
        self.label.pack(pady=10)

        self.add_portfolio_frame = tk.Frame(master, bg=style.colors.bg, padx=20, pady=20)
        self.add_portfolio_frame.pack(pady=10)

        # Entry fields for adding portfolio
        self.create_label_entry("Portfolio Name:", 0)
        self.create_label_entry("Stock Symbol:", 1)
        self.create_label_entry("Quantity:", 2)
        self.create_label_entry("Transaction Type:", 3, dropdown=True)
        self.create_label_entry("Date of Transaction (YYYY-MM-DD):", 4)
        self.create_label_entry("Price per Share:", 5)

        self.add_button = ttk.Button(self.add_portfolio_frame, text="Add Portfolio", command=self.add_portfolio, bootstyle="success")
        self.add_button.grid(row=6, columnspan=2, pady=10)

        # Update and delete buttons
        self.update_button = ttk.Button(master, text="Update Portfolio", command=self.update_portfolio, bootstyle="info")
        self.update_button.pack(pady=5)

        self.delete_button = ttk.Button(master, text="Delete Portfolio", command=self.delete_portfolio, bootstyle="danger")
        self.delete_button.pack(pady=5)

        self.get_portfolio_button = ttk.Button(master, text="Get Portfolio", command=self.get_portfolio, bootstyle="warning")
        self.get_portfolio_button.pack(pady=5)

        self.portfolios_text = tk.Text(master, height=10, width=60, font=("Arial", 12))
        self.portfolios_text.pack(pady=10)

        # Add tooltips
        ToolTip(self.add_button, "Click to add a new portfolio")
        ToolTip(self.update_button, "Click to update an existing portfolio")
        ToolTip(self.delete_button, "Click to delete a portfolio")
        ToolTip(self.get_portfolio_button, "Click to retrieve portfolio details")

    def create_label_entry(self, text, row, dropdown=False):
        tk.Label(self.add_portfolio_frame, text=text, bg=self.add_portfolio_frame.cget("background")).grid(row=row, column=0, sticky='e', pady=5)
        if dropdown:
            self.transaction_type_var = tk.StringVar(self.master)
            self.transaction_type_var.set("Buy")
            self.transaction_type_dropdown = ttk.OptionMenu(self.add_portfolio_frame, self.transaction_type_var, "Buy", "Sell")
            self.transaction_type_dropdown.grid(row=row, column=1, pady=5)
        else:
            entry = ttk.Entry(self.add_portfolio_frame)
            entry.grid(row=row, column=1, pady=5)
            setattr(self, f"{text.split()[0].lower()}_entry", entry)

    def add_portfolio(self):
        portfolio_name = self.portfolio_name_entry.get()
        symbol = self.symbol_entry.get()
        quantity = int(self.quantity_entry.get())
        transaction_type = self.transaction_type_var.get()
        date = self.date_entry.get()
        price = float(self.price_entry.get())

        transaction_data = {
            "symbol": symbol,
            "quantity": quantity,
            "transaction_type": transaction_type,
            "date": date,
            "price": price
        }

        portfolio_data = {
            "name": portfolio_name,
            "transactions": [transaction_data]
        }

        db.portfolios.insert_one(portfolio_data)
        messagebox.showinfo("Success", "Portfolio added successfully!")

    def get_portfolio(self):
        portfolio_name = simpledialog.askstring("Input", "Enter portfolio name:")
        if portfolio_name:
            portfolio = db.portfolios.find_one({"name": portfolio_name})
            if portfolio:
                self.portfolios_text.delete(1.0, tk.END)
                self.portfolios_text.insert(tk.END, f"Portfolio: {portfolio['name']}\n")
                for transaction in portfolio['transactions']:
                    self.portfolios_text.insert(tk.END, f"Symbol: {transaction['symbol']}, Quantity: {transaction['quantity']}, "
                                                         f"Transaction Type: {transaction['transaction_type']}, "
                                                         f"Date: {transaction['date']}, Price: {transaction['price']}\n")
            else:
                messagebox.showerror("Error", f"Portfolio '{portfolio_name}' not found!")
        else:
            messagebox.showwarning("Warning", "Please enter a portfolio name!")

    def update_portfolio(self):
        portfolio_name = simpledialog.askstring("Input", "Enter portfolio name:")
        if portfolio_name:
            portfolio = db.portfolios.find_one({"name": portfolio_name})
            if portfolio:
                new_symbol = self.symbol_entry.get()
                new_quantity = int(self.quantity_entry.get())
                new_transaction_type = self.transaction_type_var.get()
                new_date = self.date_entry.get()
                new_price = float(self.price_entry.get())

                new_transaction = {
                    "symbol": new_symbol,
                    "quantity": new_quantity,
                    "transaction_type": new_transaction_type,
                    "date": new_date,
                    "price": new_price
                }

                db.portfolios.update_one({"name": portfolio_name}, {"$push": {"transactions": new_transaction}})
                messagebox.showinfo("Success", "Portfolio updated successfully!")
            else:
                messagebox.showerror("Error", f"Portfolio '{portfolio_name}' not found!")
        else:
            messagebox.showwarning("Warning", "Please enter a portfolio name!")

    def delete_portfolio(self):
        portfolio_name = simpledialog.askstring("Input", "Enter portfolio name:")
        if portfolio_name:
            result = db.portfolios.delete_one({"name": portfolio_name})
            if result.deleted_count > 0:
                messagebox.showinfo("Success", f"Portfolio '{portfolio_name}' deleted successfully!")
            else:
                messagebox.showerror("Error", f"Portfolio '{portfolio_name}' not found!")
        else:
            messagebox.showwarning("Warning", "Please enter a portfolio name!")

def main():
    root = tk.Tk()
    app = PortfolioTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
