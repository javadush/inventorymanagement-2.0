import tkinter as tk
from tkinter import messagebox, simpledialog
import inventory_management as im
from linear_regression import perform_linear_regression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
from faker import Faker
import sqlite3

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management App")
        
        # Ensure the database and tables are created
        im.conn
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)
        
        # Title label
        self.title_label = tk.Label(self.main_frame, text="Inventory Management System", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)
        
        # Buttons frame
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=20)
        
        # Add item button
        self.add_item_button = tk.Button(self.buttons_frame, text="Add Item", command=self.add_item)
        self.add_item_button.grid(row=0, column=0, padx=10)
        
        # Update item button
        self.update_item_button = tk.Button(self.buttons_frame, text="Update Item", command=self.update_item)
        self.update_item_button.grid(row=0, column=1, padx=10)
        
        # Delete item button
        self.delete_item_button = tk.Button(self.buttons_frame, text="Delete Item", command=self.delete_item)
        self.delete_item_button.grid(row=0, column=2, padx=10)
        
        # View items button
        self.view_items_button = tk.Button(self.buttons_frame, text="View Items", command=self.view_items)
        self.view_items_button.grid(row=1, column=0, padx=10, pady=5)
        
        # Clear database button
        self.clear_database_button = tk.Button(self.buttons_frame, text="Clear Database", command=self.clear_database)
        self.clear_database_button.grid(row=1, column=1, padx=10, pady=5)
        
        # Generate sample data button
        self.generate_sample_data_button = tk.Button(self.buttons_frame, text="Generate Sample Data", command=self.generate_sample_data)
        self.generate_sample_data_button.grid(row=1, column=2, padx=10, pady=5)
        
        # Add order button
        self.add_order_button = tk.Button(self.buttons_frame, text="Add Order", command=self.add_order)
        self.add_order_button.grid(row=2, column=0, padx=10, pady=5)
        
        # View orders button
        self.view_orders_button = tk.Button(self.buttons_frame, text="View Orders", command=self.view_orders)
        self.view_orders_button.grid(row=2, column=1, padx=10, pady=5)
        
        # Generate sample orders button
        self.generate_sample_orders_button = tk.Button(self.buttons_frame, text="Generate Sample Orders", command=self.generate_sample_orders)
        self.generate_sample_orders_button.grid(row=2, column=2, padx=10, pady=5)
        
        # Perform linear regression button
        self.perform_regression_button = tk.Button(self.buttons_frame, text="Perform Linear Regression", command=self.perform_regression)
        self.perform_regression_button.grid(row=3, column=1, padx=10, pady=5)

    def add_item(self):
        name = simpledialog.askstring("Add Item", "Enter item name:")
        if name:
            quantity = simpledialog.askinteger("Add Item", "Enter item quantity:")
            if quantity is not None:
                price = simpledialog.askfloat("Add Item", "Enter item price:")
                if price is not None:
                    conn = sqlite3.connect('inventory.db')
                    cursor = conn.cursor()
                    
                    # Check if the item already exists
                    cursor.execute("SELECT id, quantity, price FROM inventory WHERE name = ?", (name,))
                    result = cursor.fetchone()
                    
                    if result:
                        # If the item exists, update the quantity and price
                        item_id, existing_quantity, existing_price = result
                        new_quantity = existing_quantity + quantity
                        new_price = price  # or you could implement some logic to adjust the price
                        im.update_item(item_id, name, new_quantity, new_price)
                        messagebox.showinfo("Success", "Item updated successfully.")
                    else:
                        # If the item doesn't exist, add it to the inventory
                        im.add_item(name, quantity, price)
                        messagebox.showinfo("Success", "Item added successfully.")
                    
                    conn.close()
                    self.view_items()

    def update_item(self):
        items = im.view_items()
        if not items:
            messagebox.showwarning("No Items", "No items found in inventory.")
            return
        
        item_id = simpledialog.askinteger("Update Item", "Enter item ID to update:")
        if item_id:
            for item in items:
                if item[0] == item_id:
                    name = simpledialog.askstring("Update Item", f"Enter new name for item '{item[1]}' (leave blank to keep current name):")
                    name = name if name else item[1]
                    quantity = simpledialog.askinteger("Update Item", f"Enter new quantity for item '{item[1]}' (leave blank to keep current quantity):")
                    quantity = quantity if quantity is not None else item[2]
                    price = simpledialog.askfloat("Update Item", f"Enter new price for item '{item[1]}' (leave blank to keep current price):")
                    price = price if price is not None else item[3]
                    im.update_item(item_id, name, quantity, price)
                    messagebox.showinfo("Success", "Item updated successfully.")
                    self.view_items()
                    return
            messagebox.showwarning("Item Not Found", f"Item with ID {item_id} not found in inventory.")

    def delete_item(self):
        items = im.view_items()
        if not items:
            messagebox.showwarning("No Items", "No items found in inventory.")
            return
        
        item_id = simpledialog.askinteger("Delete Item", "Enter item ID to delete:")
        if item_id:
            for item in items:
                if item[0] == item_id:
                    confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete item '{item[1]}'?")
                    if confirmation:
                        im.delete_item(item_id)
                        messagebox.showinfo("Success", "Item deleted successfully.")
                        self.view_items()
                    return
            messagebox.showwarning("Item Not Found", f"Item with ID {item_id} not found in inventory.")

    def view_items(self):
        items = im.view_items()
        if items:
            top = tk.Toplevel()
            top.title("View Items")
            frame = tk.Frame(top)
            frame.pack(padx=20, pady=20)
            for idx, item in enumerate(items):
                tk.Label(frame, text=f"ID: {item[0]} - Name: {item[1]} - Quantity: {item[2]} - Price: ${item[3]:.2f}").pack(anchor='w')
        else:
            messagebox.showinfo("No Items", "No items found in inventory.")

    def clear_database(self):
        confirmation = messagebox.askyesno("Clear Database", "Are you sure you want to clear the database? This action cannot be undone.")
        if confirmation:
            im.clear_database()
            messagebox.showinfo("Success", "Database cleared successfully.")
        else:
            messagebox.showinfo("Cancelled", "Database clear operation cancelled.")

    def generate_sample_data(self):
        num_items = simpledialog.askinteger("Generate Sample Data", "Enter number of sample items to generate:")
        if num_items:
            im.generate_sample_data(num_items)
            messagebox.showinfo("Success", f"{num_items} sample items generated successfully.")
            self.view_items()

    def add_order(self):
        items = im.view_items()
        if not items:
            messagebox.showwarning("No Items", "No items found in inventory.")
            return
        
        item_id = simpledialog.askinteger("Add Order", "Enter item ID for the order:")
        if item_id:
            item_exists = any(item[0] == item_id for item in items)
            if not item_exists:
                messagebox.showwarning("Item Not Found", f"Item with ID {item_id} not found in inventory.")
                return
            
            quantity = simpledialog.askinteger("Add Order", "Enter quantity for the order:")
            if quantity is not None:
                order_date = simpledialog.askstring("Add Order", "Enter order date (YYYY-MM-DD):")
                if order_date:
                    im.add_order(item_id, quantity, order_date)
                    messagebox.showinfo("Success", "Order added successfully.")
                    self.view_orders()

    def view_orders(self):
        orders = im.view_orders()
        if orders:
            top = tk.Toplevel()
            top.title("View Orders")
            frame = tk.Frame(top)
            frame.pack(padx=20, pady=20)
            for idx, order in enumerate(orders):
                tk.Label(frame, text=f"ID: {order[0]} - Item: {order[1]} - Quantity: {order[2]} - Date: {order[3]}").pack(anchor='w')
        else:
            messagebox.showinfo("No Orders", "No orders found.")

    def generate_sample_orders(self):
        items = im.view_items()
        if not items:
            messagebox.showwarning("No Items", "No items found in inventory.")
            return
    
        num_orders = simpledialog.askinteger("Generate Sample Orders", "Enter number of sample orders to generate:")
        if num_orders:
            for _ in range(num_orders):
                item_id = random.choice([item[0] for item in items])  # Randomly choose item ID from available items
                quantity = random.randint(1, 10)
                order_date = Faker().date_this_year().isoformat()
                im.add_order(item_id, quantity, order_date)
        
            messagebox.showinfo("Success", f"{num_orders} sample orders generated successfully.")
            self.view_orders()
    
    def perform_regression(self):
        orders = im.view_orders()
        if not orders:
            messagebox.showwarning("No Orders", "No orders found in the database.")
            return
        
        try:
            data = [(order[2], order[3]) for order in orders]
            X = [float(d[0]) for d in data]
            y = [float(d[1]) for d in data]
        
            model = perform_linear_regression(data)  # Use the imported function correctly
            slope, intercept = model.coef_[0], model.intercept_
        
            plt.figure(figsize=(8, 6))
            plt.scatter(X, y, color='blue', label='Data points')
            plt.plot(X, model.predict(np.array(X).reshape(-1, 1)), color='red', linewidth=2, label=f'Regression Line: y = {slope:.2f}x + {intercept:.2f}')
            plt.title('Linear Regression Analysis')
            plt.xlabel('Quantity')
            plt.ylabel('Price')
            plt.legend()
        
            # Display plot in Tkinter window
            top = tk.Toplevel()
            top.title("Linear Regression Analysis")
            canvas = FigureCanvasTkAgg(plt.gcf(), master=top)
            canvas.draw()
            canvas.get_tk_widget().pack()
        
            plt.show()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error performing linear regression: {str(e)}")

# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

