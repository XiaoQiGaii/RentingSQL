import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import mysql.connector
from decimal import Decimal

# Database connection setup
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="341062",
        database="RentSys"
    )

# Function to check if the reservation date is valid
def check_reservation_time(SYear, EYear, SMonth, EMonth, SDay, EDay):
    if SYear > EYear:
        messagebox.showerror("Error", "Invalid reservation time.")
        return False
    elif SYear == EYear:
        if SMonth > EMonth:
            messagebox.showerror("Error", "Invalid reservation time.")
            return False
        elif SMonth == EMonth:
            if SDay >= EDay:
                messagebox.showerror("Error", "Invalid reservation time.")
                return False
            else:
                return True
        else:
            return True
    else:
        return True

# Function to calculate the rental price, applying discounts if needed
def calculate_price(cartype, start_date, end_date):
    days_rented = (end_date - start_date).days
    connection = connect_to_db()
    cursor = connection.cursor()

    # Get the daily rate for the selected car type
    cursor.execute("SELECT DailyRate FROM Pricing WHERE Cartype = %s", (cartype,))
    rate = cursor.fetchone()
    if not rate:
        messagebox.showerror("Error", f"No pricing found for {cartype}")
        return None
    daily_rate = Decimal(rate[0])  # Ensure daily_rate is a Decimal

    # Calculate total price
    total_price = days_rented * daily_rate

    # Apply 10% discount if the rental is 7 days or longer
    if days_rented >= 7:
        total_price *= Decimal('0.90')  # Convert 0.90 to Decimal

    connection.close()
    return total_price

# Function to submit the reservation
def submit_reservation():
    RName = RName_entry.get()
    Cartype = Cartype_entry.get()
    StartDate_str = StartDate_entry.get()
    EndDate_str = EndDate_entry.get()
    try:
        StartDate = datetime.strptime(StartDate_str, '%Y-%m-%d')
        EndDate = datetime.strptime(EndDate_str, '%Y-%m-%d')
        SYear = StartDate.year
        EYear = EndDate.year
        SMonth = StartDate.month
        EMonth = EndDate.month
        SDay = StartDate.day
        EDay = EndDate.day
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    # Check if reservation is valid
    if not check_reservation_time(SYear, EYear, SMonth, EMonth, SDay, EDay):
        return
    
    if not check_reservation_time(SYear, EYear, SMonth, EMonth, SDay, EDay):
        return
    
    if not check_for_conflict(Cartype, EndDate):
        messagebox.showerror("Error", "Cannot extend. Another reservation exists for this car type.")
        return


    # Calculate price
    Price = calculate_price(Cartype, StartDate, EndDate)
    if Price is None:
        return

    # Insert reservation into the database
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = "INSERT INTO Reservations (RName, Cartype, StartDate, EndDate, Price) VALUES (%s, %s, %s, %s, %s)"
        values = (RName, Cartype, StartDate_str, EndDate_str, Price)

        cursor.execute(query, values)
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Reservation submitted successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error occurred: {err}")

# Function to check for conflicting reservations
def check_for_conflict(cartype, EndDate):
    connection = connect_to_db()
    cursor = connection.cursor()

    # SQL query to check for conflicts
    query = """
    SELECT COUNT(*) FROM Reservations 
    WHERE Cartype = %s AND StartDate < %s AND EndDate > NOW()
    """
    cursor.execute(query, (cartype, EndDate))
    count = cursor.fetchone()[0]

    connection.close()

    # If there are any conflicting reservations, return False
    if count > 0:
        return False
    return True

# Function to request an extension
def request_extension():
    RName = RName_entry.get()
    Cartype = Cartype_entry.get()
    NewEndDate_str = NewEndDate_entry.get()

    try:
        NewEndDate = datetime.strptime(NewEndDate_str, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    # Check for conflicting reservations for the same vehicle type
    if not check_for_conflict(Cartype, NewEndDate):
        messagebox.showerror("Error", "Cannot extend. Another reservation exists for this car type.")
        return

    # Update the reservation in the database
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # Update the EndDate for the reservation
        query = "UPDATE Reservations SET EndDate = %s WHERE RName = %s AND Cartype = %s"
        cursor.execute(query, (NewEndDate_str, RName, Cartype))

        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Reservation extended successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error occurred: {err}")

# GUI setup for reservation and extension request
root = tk.Tk()
root.title("Car Rental Reservation System")

tk.Label(root, text="Renter Name").grid(row=0, column=0)
tk.Label(root, text="Car Type (sedan, SUV, pickup, van)").grid(row=1, column=0)
tk.Label(root, text="Start Date (YYYY-MM-DD)").grid(row=2, column=0)
tk.Label(root, text="End Date (YYYY-MM-DD)").grid(row=3, column=0)

RName_entry = tk.Entry(root)
Cartype_entry = tk.Entry(root)
StartDate_entry = tk.Entry(root)
EndDate_entry = tk.Entry(root)

RName_entry.grid(row=0, column=1)
Cartype_entry.grid(row=1, column=1)
StartDate_entry.grid(row=2, column=1)
EndDate_entry.grid(row=3, column=1)

# Submit button for reservation
submit_button = tk.Button(root, text="Submit Reservation", command=submit_reservation)
submit_button.grid(row=4, column=1)

# Extension request setup
tk.Label(root, text="New End Date (YYYY-MM-DD)").grid(row=5, column=0)
NewEndDate_entry = tk.Entry(root)
NewEndDate_entry.grid(row=5, column=1)

# Submit button for extension request
extension_button = tk.Button(root, text="Request Extension", command=request_extension)
extension_button.grid(row=6, column=1)

root.mainloop()
