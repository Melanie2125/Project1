import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime

root = tk.Tk()

root.geometry("765x800")
root.title("Pet Grooming Shop Management System")
root.configure(bg='lightblue')

style = ttk.Style()

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)
style.configure('TNotebook.Tab', font=('Comic Sans MS', 11))

style.configure('TNotebook.Tab',
                foreground='#6495ED',
                font=('Comic Sans MS', 12),
                padding=[10, 5])

home_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(home_frame, text="Home")

header = tk.Label(home_frame, text="Welcome to The Pet Grooming Shop Management System!", bg='lightblue', font=('Comic Sans MS', 18))
header.pack(padx=20, pady=20)

desc_label = tk.Label(
    home_frame,
    text="Easily schedule, view, update, and cancel your pet grooming appointments.\n"
         "Manage your pet's information and explore available grooming services—all in one place!",
    bg='lightblue',
    font=('Comic Sans MS', 12),
)
desc_label.pack(pady=(0, 20))

image_pet_grooming = Image.open("photos/pet-photo.jpg")
image_pet_grooming = image_pet_grooming.resize((300, 150))
photo_pet_grooming = ImageTk.PhotoImage(image_pet_grooming)

image_grooming = tk.Label(home_frame, image=photo_pet_grooming, bg='#f9f9f9')
image_grooming.pack(pady=20)

features_text = (
    "•  Create new appointments, add pets, and enter your customer information.\n"
    "•  Review your appointments, personal details, pet profiles, and available services.\n"
    "•  Update your information, pet details, or modify existing appointments.\n"
    "•  Delete your account, pets, or appointments if needed."
)

features_label = tk.Label(home_frame, text=features_text, font=('Comic Sans MS', 12), justify='left', bg='lightblue')
features_label.pack(padx=20, pady=10)

image_dog = Image.open("photos/dog-photo.jpg")
image_dog = image_dog.resize((300, 150))
photo_dog = ImageTk.PhotoImage(image_dog)

image_dog = tk.Label(home_frame, image=photo_dog, bg='#f9f9f9')
image_dog.pack(pady=20)




# Create Tab
create_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(create_frame, text="Create Appointment & Info")

tk.Label(
    create_frame,
    text="Fill out the form below to create a new appointment.",
    font=('Comic Sans MS', 14, 'bold'),
    bg='lightblue'
).pack(pady=(10, 5))

columns_frame = tk.Frame(create_frame, bg='lightblue')
columns_frame.pack()


# Column 1: Customer Info
customer_frame = tk.Frame(columns_frame, bg='lightblue')
customer_frame.pack(side='left', padx=20)

tk.Label(customer_frame, text="Customer ID (Used to Identify You! Numbers only!)", bg='lightblue').pack(fill='x')
customer_id_entry = tk.Entry(customer_frame)
customer_id_entry.pack(pady=5)

tk.Label(customer_frame, text="Customer First Name", bg='lightblue').pack(fill='x')
first_name_entry = tk.Entry(customer_frame)
first_name_entry.pack(pady=5)

tk.Label(customer_frame, text="Customer Last Name", bg='lightblue').pack(fill='x')
last_name_entry = tk.Entry(customer_frame)
last_name_entry.pack(pady=5)

tk.Label(customer_frame, text="Phone Number (XXX-XXX-XXXX)", bg='lightblue').pack(fill='x')
phone_entry = tk.Entry(customer_frame)
phone_entry.pack(pady=5)

# Column 2: Pet Info
pet_frame = tk.Frame(columns_frame, bg='lightblue')
pet_frame.pack(side='left', padx=20)

tk.Label(pet_frame, text="Pet Name", bg='lightblue').pack(fill='x')
pet_name_entry = tk.Entry(pet_frame)
pet_name_entry.pack(pady=5)

tk.Label(pet_frame, text="Birthday (YYYY-MM-DD)", bg='lightblue').pack(fill='x')
pet_bday_entry = tk.Entry(pet_frame)
pet_bday_entry.pack(pady=5)

tk.Label(pet_frame, text="Pet Type", bg='lightblue').pack(fill='x')
pet_type_entry = tk.Entry(pet_frame)
pet_type_entry.pack(pady=5)

# Column 3: Appointment Info
appt_frame = tk.Frame(columns_frame, bg='lightblue')
appt_frame.pack(side='left', padx=20)

tk.Label(appt_frame, text="Appointment Date (YYYY-MM-DD)", bg='lightblue').pack(fill='x')
appt_date_entry = tk.Entry(appt_frame)
appt_date_entry.pack(pady=5)

tk.Label(appt_frame, text="Time (HH:MM:SS)", bg='lightblue').pack(fill='x')
appt_time_entry = tk.Entry(appt_frame)
appt_time_entry.pack(pady=5)

tk.Label(appt_frame, text="Service", bg='lightblue').pack(fill='x')
service_selec = ttk.Combobox(appt_frame, values=["Bathing", "Grooming", "Nail Trimming", "Check-up"])
service_selec.pack(pady=5)




def create_appointment_add_info():
    user_id = customer_id_entry.get()
    fname = first_name_entry.get()
    lname = last_name_entry.get()
    phone = phone_entry.get()
    pet_name = pet_name_entry.get()
    pet_bday = pet_bday_entry.get()
    pet_type = pet_type_entry.get()
    appt_date = appt_date_entry.get()
    appt_time = appt_time_entry.get()
    service = service_selec.get()

    # Connecting to the database
    conn = sqlite3.connect("proj1.db")
    cur = conn.cursor()

    # Checks if the customer_id entered already exists in the Customers table
    cur.execute("SELECT customer_id FROM Customers WHERE customer_id = ?", (user_id,))
    result = cur.fetchone()

    if result:
        messagebox.showerror("Error", "Customer ID already exists. Please choose a different ID.")
        conn.close()
        return

    # Creates new Customer with the provided user_id
    cur.execute("INSERT INTO Customers (customer_id, first_name, last_name, phone_number) VALUES (?, ?, ?, ?)",
                (user_id, fname, lname, phone))

    # Inserts the pet into Pets table
    cur.execute("INSERT INTO Pets (name, birthday, type, customer_id) VALUES (?, ?, ?, ?)",
                (pet_name, pet_bday, pet_type, user_id))

    pet_id = cur.lastrowid  # SQLite assigned the id to the pet

    # Get service_id based on selected service
    cur.execute("SELECT service_id FROM Services WHERE service_type = ?", (service,))
    service_id = cur.fetchone()[0]

    # Generates appointment_id
    appt_id = fname[:1].lower() + lname[:1].lower() + str(int(datetime.now().timestamp()))[-4:]

    # Insert the create appointment into Appointments table
    cur.execute("INSERT INTO Appointments (appointment_id, date, time, status, customer_id, pet_id, service_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (appt_id, appt_date, appt_time, 'Scheduled', user_id, pet_id, service_id))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Appointment created successfully! The ID of your pet is: " + str(pet_id) + ". Your appointment ID is: " + str(appt_id) + ".")


tk.Button(create_frame, text="Create Appointment", command=create_appointment_add_info).pack(pady=15)



# 2 images at the bottom
image_cat = Image.open("photos/cat-photo.jpg")
image_cat = image_cat.resize((300, 150))
photo_cat = ImageTk.PhotoImage(image_cat)

image_cat = tk.Label(create_frame, image=photo_cat)
image_cat.pack(pady=15)

image_fish = Image.open("photos/fish-photo.jpg")
image_fish = image_fish.resize((300, 150))
photo_fish = ImageTk.PhotoImage(image_fish)

image_fish = tk.Label(create_frame, image=photo_fish)
image_fish.pack(pady=15)


# Read Tab
read_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(read_frame, text="Review your Info")

# Update Tab
update_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(update_frame, text="Update your Info")

# Delete Tab
delete_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(delete_frame, text="Delete your Info")

root.mainloop()
