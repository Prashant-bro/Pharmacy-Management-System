import mysql.connector
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox

# Create connection to the database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="CODER",
  database="project",
  charset="latin1"
)

# Create cursor object to execute queries
cursor = db.cursor()

# Create GUI window
window = tk.Tk()
window.title("Pharmacy Shop")
window.geometry("1600x1200")
#To Add Background colour
background_frame=tk.Frame(window,bg='light blue')
background_frame.place(relwidth=1,relheight=1)


abc_label = tk.Label(window, text="PHARMACY MANAGEMENT SYSTEM", font=("Algerian", 40))
abc_label.place(x=380, y=40)

# Create label for search box
search_label = tk.Label(window, text="Search Medicine:", font=("Arial", 14))
search_label.place(x=50, y=150)

# Create search box
search_box = tk.Entry(window, font=("Arial", 14), width=70)
search_box.place(x=220, y=150)

# Create function to search for medicine
def search_medicine():
    # Execute search query
    search_term = search_box.get()
    query = f"SELECT * FROM medicine WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Display search results
    if len(results) > 0:
        # Create section table
        section_label = tk.Label(window, text="batch no.", font=("Arial", 14))
        section_label.place(x=50, y=200)
        quantity_label = tk.Label(window, text="Quantity", font=("Arial", 14))
        quantity_label.place(x=150, y=200)
        price_label = tk.Label(window, text="Price", font=("Arial", 14))
        price_label.place(x=250, y=200)
        price_label=tk.Label(window, text="expiry_date", font=("Arial", 14))
        price_label.place(x=350, y=200)
        
        # Display search results
        row = 250
        for result in results:
            name = result[1]
            section = result[2]
            quantity = result[5]
            price = result[4]
            expiry_date=result[3]
            section_label = tk.Label(window, text=section, font=("Arial", 12))
            section_label.place(x=50, y=row)
            quantity_label = tk.Label(window, text=quantity, font=("Arial", 12))
            quantity_label.place(x=150, y=row)
            price_label = tk.Label(window, text=price, font=("Arial", 12))
            price_label.place(x=250, y=row)
            price_label = tk.Label(window, text=expiry_date, font=("Arial", 12))
            price_label.place(x=350, y=row) 
            row += 40
    else:
        # Display error message
        error_label = tk.Label(window, text="No results found.", font=("Arial", 14))
        error_label.place(x=50, y=250)

# Create "Search" button
search_button = tk.Button(window, text="Search", font=("Arial", 24), command=search_medicine, width=10, height=1)
search_button.place(x=650, y=500)

# Create "Add" button
def add_medicine():
    # Create a new pop-up window for adding a medicine
    add_window = Toplevel(window)
    add_window.title("Add Medicine")
    add_window.geometry("400x300")
    
    # Create labels and entry widgets for medicine details
    name_label = Label(add_window, text="Name:")
    name_label.pack()
    name_entry = Entry(add_window)
    name_entry.pack()
    
    expiry_label = Label(add_window, text="Expiry Date:")
    expiry_label.pack()
    expiry_entry = Entry(add_window)
    expiry_entry.pack()
    
    batch_label = Label(add_window, text="Batch Number:")
    batch_label.pack()
    batch_entry = Entry(add_window)
    batch_entry.pack()
    
    price_label = Label(add_window, text="Price:")
    price_label.pack()
    price_entry = Entry(add_window)
    price_entry.pack()
    
    quantity_label = Label(add_window, text="Quantity:")
    quantity_label.pack()
    quantity_entry = Entry(add_window)
    quantity_entry.pack()
    
    section_label = Label(add_window, text="Section:")
    section_label.pack()
    section_entry = Entry(add_window)
    section_entry.pack()
    
    # Function to add the medicine to the database
    def save_medicine():
        name = name_entry.get()
        expiry = expiry_entry.get()
        batch = batch_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()
        section = section_entry.get()
        
        # Insert the medicine into the database
        query = "INSERT INTO medicine (name, expiry_date, batch_number, price, quantity, section) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, expiry, batch, price, quantity, section)
        cursor.execute(query, values)
        db.commit()
        
        # Close the pop-up window
        add_window.destroy()
    
    # Create a "Save" button to save the medicine
    save_button = Button(add_window, text="Save", command=save_medicine)
    save_button.pack()

add_button = tk.Button(window, text="Add", font=("Arial", 24), command=add_medicine, width=10, height=1)
add_button.place(x=150, y=500)

# Create "Delete" button
def delete_medicine():
    # Create a new pop-up window for deleting a medicine
    delete_window = Toplevel(window)
    delete_window.title("Delete Medicine")
    delete_window.geometry("500x100")
    
    # Create label and entry widget for entering the medicine name to delete
    delete_label = Label(delete_window, text="Enter the name of the medicine to delete:")
    delete_label.pack()
    delete_entry = Entry(delete_window)
    delete_entry.pack()
    
    # Function to delete the medicine from the database
    def confirm_delete():
        name_to_delete = delete_entry.get()
        
        # Check if the medicine exists in the database
        cursor.execute("SELECT * FROM medicine WHERE name = %s", (name_to_delete,))
        existing_medicine = cursor.fetchone()
        
        if existing_medicine:
            # Delete the medicine
            cursor.execute("DELETE FROM medicine WHERE name = %s", (name_to_delete,))
            db.commit()
            messagebox.showinfo("Success", f"The medicine '{name_to_delete}' has been deleted.")
        else:
            messagebox.showerror("Error", f"The medicine '{name_to_delete}' does not exist.")
        
        # Close the pop-up window
        delete_window.destroy()
    
    # Create a "Delete" button to confirm the deletion
    delete_button = Button(delete_window, text="Delete", command=confirm_delete)
    delete_button.pack()

delete_button = tk.Button(window, text="Delete", font=("Arial", 24), command=delete_medicine, width=10, height=1)
delete_button.place(x=400, y=500)

# Run the window
window.mainloop()

# Close the database connection when the window is closed
db.close()
