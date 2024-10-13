import tkinter as tk
from tkinter import ttk
import mysql.connector

# Database connection setup
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="341062",
        database="RentSys"
    )

# Function to fetch and display reservation details
def show_reservations():
    connection = connect_to_db()
    cursor = connection.cursor()

    # Fetch all reservation details from the database
    cursor.execute("SELECT RName, Cartype, StartDate, EndDate, Price FROM Reservations")
    rows = cursor.fetchall()

    # Clear the Treeview table before adding new rows
    for row in tree.get_children():
        tree.delete(row)

    # Insert each row from the database into the Treeview
    for row in rows:
        tree.insert("", "end", values=row)

    connection.close()

# GUI setup for displaying reservation details
root = tk.Tk()
root.title("Reservation Details - Mr. Johnson's View")

# Set up the Treeview (table) widget
tree = ttk.Treeview(root, columns=("Renter Name", "Car Type", "Start Date", "End Date", "Price"), show='headings')
tree.heading("Renter Name", text="Renter Name")
tree.heading("Car Type", text="Car Type")
tree.heading("Start Date", text="Start Date")
tree.heading("End Date", text="End Date")
tree.heading("Price", text="Price")

# Set the column widths
tree.column("Renter Name", width=120)
tree.column("Car Type", width=100)
tree.column("Start Date", width=150)
tree.column("End Date", width=150)
tree.column("Price", width=80)

# Add the Treeview to the window and pack it
tree.pack(fill="both", expand=True)

# Button to refresh and show the latest reservations
refresh_button = tk.Button(root, text="Refresh", command=show_reservations)
refresh_button.pack(pady=10)

# Call the function to show reservations on startup
show_reservations()

root.mainloop()
