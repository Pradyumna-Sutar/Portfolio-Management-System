import tkinter as tk
from tkinter import messagebox, simpledialog
from ttkbootstrap import Style, ttk
from PIL import Image, ImageTk
from database import Database
from tooltip import ToolTip
from gui_elements import create_label_entry

MONGODB_URI = "mongodb+srv://romocromo90:romocromo9@cluster0.atmpzxm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "portfolio_tracker"

class PortfolioTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Portfolio Management")

        self.db = Database(MONGODB_URI, DATABASE_NAME)

        style = Style(theme='cosmo')
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TFrame", background=style.colors.bg)

        self.background_image = Image.open("2.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(master, text="Welcome to Portfolio Management", font=("Arial", 18, "bold"), bg=style.colors.bg)
        self.label.pack(pady=10)

        self.add_portfolio_frame = tk.Frame(master, bg=style.colors.bg, padx=20, pady=20)
        self.add_portfolio_frame.pack(pady=10)

        self.portfolio_name_entry = create_label_entry(self.add_portfolio_frame, "Portfolio Name:", 0, master)
        self.symbol_entry = create_label_entry(self.add_portfolio_frame, "Stock Symbol:", 1, master)
        self.quantity_entry = create_label_entry(self.add_portfolio_frame, "Quantity:", 2, master)
        self.transaction_type_var = create_label_entry(self.add_portfolio_frame, "Transaction Type:", 3, master, dropdown=True)
        self.date_entry = create_label_entry(self.add_portfolio_frame, "Date of Transaction (YYYY-MM-DD):", 4, master)
        self.price_entry = create_label_entry(self.add_portfolio_frame, "Price per Share:", 5, master)

        self.add_button = ttk.Button(self.add_portfolio_frame, text="Add Portfolio", command=self.add_portfolio, bootstyle="success")
        self.add_button.grid(row=6, columnspan=2, pady=10)

        self.update_button = ttk.Button(master, text="Update Portfolio", command=self.update_portfolio, bootstyle="info")
        self.update_button.pack(pady=5)

        self.delete_button = ttk.Button(master, text="Delete Portfolio", command=self.delete_portfolio, bootstyle="danger")
        self.delete_button.pack(pady=5)

        self.get_portfolio_button = ttk.Button(master, text="Get Portfolio", command=self.get_portfolio, bootstyle="warning")
        self.get_portfolio_button.pack(pady=5)

        self.portfolios_text = tk.Text(master, height=10, width=60, font=("Arial", 12))
        self.portfolios_text.pack(pady=10)

        ToolTip(self.add_button, "Click to add a new portfolio")
        ToolTip(self.update_button, "Click to update an existing portfolio")
        ToolTip(self.delete_button, "Click to delete a portfolio")
        ToolTip(self.get_portfolio_button, "Click to retrieve portfolio details")

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

        self.db.insert_portfolio(portfolio_data)
        messagebox.showinfo("Success", "Portfolio added successfully!")

    def get_portfolio(self):
        portfolio_name = simpledialog.askstring("Input", "Enter portfolio name:")
        if portfolio_name:
            portfolio = self.db.find_portfolio(portfolio_name)
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
            portfolio = self.db.find_portfolio(portfolio_name)
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

                self.db.update_portfolio(portfolio_name, new_transaction)
                messagebox.showinfo("Success", "Portfolio updated successfully!")
            else:
                messagebox.showerror("Error", f"Portfolio '{portfolio_name}' not found!")
        else:
            messagebox.showwarning("Warning", "Please enter a portfolio name!")

    def delete_portfolio(self):
        portfolio_name = simpledialog.askstring("Input", "Enter portfolio name:")
        if portfolio_name:
            result = self.db.delete_portfolio(portfolio_name)
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
