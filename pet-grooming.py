import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime

root = tk.Tk()

root.geometry("780x800")
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

header = tk.Label(home_frame, text="Welcome to The Pet Grooming Shop Management System!", bg='lightblue', font=('Comic Sans MS', 18, 'bold'))
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
create_frame = tk.LabelFrame(notebook, bg='lightblue')
notebook.add(create_frame, text="Create Appointment & Info")

tk.Label(
    create_frame,
    text="Fill out the form below to create a new appointment.",
    font=('Comic Sans MS', 14, 'bold'),
    bg='lightblue'
).pack(pady=(10, 5))

columns_frame = tk.Frame(create_frame, bg='lightblue')
columns_frame.pack()


# Customer Info Box
customer_frame = tk.LabelFrame(columns_frame, bg='lightblue')
customer_frame.pack(side='left', padx=20)

customer_frame = tk.LabelFrame(
    columns_frame,
    text="Customer Enter Info",
    bg='lightblue',
    font=('Arial', 10, 'bold')
)
customer_frame.pack(side='left', padx=20, pady=10)

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



# Pet Info Box
pet_frame = tk.LabelFrame(
    columns_frame,
    text="Pet Enter Info",
    bg='lightblue',
    font=('Arial', 10, 'bold')
)
pet_frame.pack(side='left', padx=20, pady=10)

tk.Label(pet_frame, text="Pet Name", bg='lightblue').pack(fill='x')
pet_name_entry = tk.Entry(pet_frame)
pet_name_entry.pack(pady=5)

tk.Label(pet_frame, text="Birthday (YYYY-MM-DD)", bg='lightblue').pack(fill='x')
pet_bday_entry = tk.Entry(pet_frame)
pet_bday_entry.pack(pady=5)

tk.Label(pet_frame, text="Pet Type", bg='lightblue').pack(fill='x')
pet_type_entry = tk.Entry(pet_frame)
pet_type_entry.pack(pady=5)



# Appointment Info Box
appt_frame = tk.LabelFrame(
    columns_frame,
    text="Appointment Enter Info",
    bg='lightblue',
    font=('Arial', 10, 'bold')
)
appt_frame.pack(side='left', padx=20, pady=10)

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

    if not all([user_id, fname, lname, phone, pet_name, pet_bday, pet_type, appt_date, appt_time, service]):
        messagebox.showerror("Error", "Please fill in all fields before submitting.")
        return

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
image_frame = tk.Frame(create_frame, bg='lightblue')
image_frame.pack(pady=15)

image_cat = Image.open("photos/cat-photo.jpg")
image_cat = image_cat.resize((300, 150))
photo_cat = ImageTk.PhotoImage(image_cat)

label_cat = tk.Label(image_frame, image=photo_cat, bg='lightblue')
label_cat.pack(side='left', padx=10)

image_fish = Image.open("photos/fish-photo.jpg")
image_fish = image_fish.resize((300, 150))
photo_fish = ImageTk.PhotoImage(image_fish)

label_fish = tk.Label(image_frame, image=photo_fish, bg='lightblue')
label_fish.pack(side='left', padx=10)




# Read Tab
read_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(read_frame, text="Review your Info")

tk.Label(
    read_frame,
    text="Review Your Information and Services we Offer!",
    font=('Comic Sans MS', 16, 'bold'),
    bg='lightblue'
).pack(pady=(10, 10))

info_columns = tk.Frame(read_frame, bg='lightblue')
info_columns.pack(padx=20, pady=10)


# Appointment Info Entry Box
appt_frame = tk.LabelFrame(info_columns, text="Appointment Info", bg='lightblue', font=('Arial', 10, 'bold'))
appt_frame.grid(row=0, padx=10, pady=10)

tk.Label(appt_frame, text="Appointment ID", bg='lightblue').grid(row=0)
appt_id_entry = tk.Entry(appt_frame)
appt_id_entry.grid(row=1, pady=5)

tk.Label(appt_frame, text="First Name", bg='lightblue').grid(row=2)
fname_entry = tk.Entry(appt_frame)
fname_entry.grid(row=3, pady=5)

tk.Label(appt_frame, text="Last Name", bg='lightblue').grid(row=4)
lname_entry = tk.Entry(appt_frame)
lname_entry.grid(row=5, pady=5)

def show_appointment():
    appt_id = appt_id_entry.get()
    fname = fname_entry.get().lower().strip()
    lname = lname_entry.get().lower().strip()
    
    conn = sqlite3.connect("proj1.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            a.appointment_id,
            c.first_name,
            c.last_name,
            a.date,
            a.time,
            a.status,
            st.service_type,
            st.price,
            st.duration,
            st.description,
            s.provider_name,
            s.tools_used,
            p.name AS pet_name
        FROM Appointments a
        JOIN Customers c ON a.customer_id = c.customer_id
        JOIN Pets p ON a.pet_id = p.pet_id
        JOIN Services s ON a.service_id = s.service_id
        JOIN ServiceTypes st ON s.service_type = st.service_type
        WHERE a.appointment_id = ?
            AND LOWER(c.first_name) = ?
            AND LOWER(c.last_name) = ?
    """, (appt_id, fname, lname))

    result = cursor.fetchone()
    conn.close()

    if result:
        (appt_id, first_name, last_name, date, time, status,
            service_type, price, duration, description,
            provider_name, tools_used, pet_name) = result

        messagebox.showinfo(
            "Appointment Details",
            f"Appointment ID: {appt_id}\n"
            f"Customer: {first_name} {last_name}\n"
            f"Pet: {pet_name}\n\n"
            f"Service: {service_type}\n"
            f"Description: {description}\n"
            f"Provider: {provider_name}\n"
            f"Tools Used: {tools_used}\n"
            f"Price: ${price:.2f}\n"
            f"Duration: {duration} minutes\n\n"
            f"Date: {date}\n"
            f"Time: {time}\n"
            f"Status: {status}"
        )
    else:
        messagebox.showwarning("Not Found", "Appointment not found. Please check your info")


tk.Button(appt_frame, text="Show Your Appointment!", command=show_appointment).grid(row=6, pady=10)



# Customer Info Entry Box
cust_frame = tk.LabelFrame(info_columns, text="Customer Info", bg='lightblue', font=('Arial', 10, 'bold'))
cust_frame.grid(row=0, column=1, padx=10, pady=10)

tk.Label(cust_frame, text="Customer ID", bg='lightblue').grid(row=0)
appointment_id_entry = tk.Entry(cust_frame)
appointment_id_entry.grid(row=1, pady=5)

tk.Label(cust_frame, text="First Name", bg='lightblue').grid(row=2)
first_name_read_entry = tk.Entry(cust_frame)
first_name_read_entry.grid(row=3, pady=5)

tk.Label(cust_frame, text="Last Name", bg='lightblue').grid(row=4)
last_name_read_entry = tk.Entry(cust_frame)
last_name_read_entry.grid(row=5, pady=5)


def show_customer_info():
    customer_id = appointment_id_entry.get()
    fname = first_name_read_entry.get().lower()
    lname = last_name_read_entry.get().lower()

    conn = sqlite3.connect("proj1.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, first_name, last_name, phone_number
        FROM Customers
        WHERE customer_id = ?
            AND LOWER(first_name) = ?
            AND LOWER(last_name) = ?
    """, (customer_id, fname, lname))

    result = cursor.fetchone()

    if result:
        cid, fname, lname, phone = result

        messagebox.showinfo(
            "Your Customer Info",
            f"Customer ID: {cid}\n"
            f"Name: {fname} {lname}\n"
            f"Phone: {phone}"
        )
    else:
        messagebox.showwarning("Not Found", "Customer not found. Please check your info.")


tk.Button(cust_frame, text="Show My Information!", command=show_customer_info).grid(row=6, pady=10)



# Pet Info Entry Box
pet_frame = tk.LabelFrame(info_columns, text="Pet Info", bg='lightblue', font=('Arial', 10, 'bold'))
pet_frame.grid(row=0, column=2, padx=10, pady=10, sticky='n')

tk.Label(pet_frame, text="Pet ID", bg='lightblue').grid(row=0)
pet_id_entry = tk.Entry(pet_frame)
pet_id_entry.grid(row=1, pady=5)

tk.Label(pet_frame, text="Pet Name", bg='lightblue').grid(row=2)
pet_name_read_entry = tk.Entry(pet_frame)
pet_name_read_entry.grid(row=3, pady=5)


def show_pet_info():
    pet_id = pet_id_entry.get()
    name = pet_name_read_entry.get().lower()

    conn = sqlite3.connect("proj1.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.pet_id, p.name, p.birthday, p.type, c.first_name, c.last_name
        FROM Pets p
        JOIN Customers c ON p.customer_id = c.customer_id
        WHERE p.pet_id = ?
            AND LOWER(p.name) = ?
    """, (pet_id, name))

    result = cursor.fetchone()

    if result:
        pet_id, name, birthday, pet_type, first_name, last_name = result

        messagebox.showinfo(
            "Your Pet Info",
            f"Pet ID: {pet_id}\n"
            f"Pet Name: {name}\n"
            f"Birthday: {birthday}\n"
            f"Type: {pet_type}\n"
            f"Owner: {first_name} {last_name}"
        )
    else:
        messagebox.showwarning("Not Found", "Pet not found. Please check your info.")

    conn.close()


tk.Button(pet_frame, text="Show My Pet Information!", command=show_pet_info).grid(row=4, pady=10)


def show_services():
    conn = sqlite3.connect("proj1.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.service_type, s.provider_name, s.tools_used, st.price, st.duration, st.description
        FROM Services s
        JOIN ServiceTypes st ON s.service_type = st.service_type
    """)

    result = cursor.fetchall()

    if result:
        services_info = ""
        for row in result:
            service_type, provider_name, tools_used, price, duration, description = row
            services_info += (
                f"Service Type: {service_type}\n"
                f"Provider Name: {provider_name}\n"
                f"Tools Used: {tools_used}\n"
                f"Price: ${price:.2f}\n"
                f"Duration: {duration} minutes\n"
                f"Description: {description}\n\n"
            )
        messagebox.showinfo("Services Our Pet Grooming Shop Offers", services_info)

    conn.close()


# Services Button will Join Services and ServiceTypes Tables and show Info
tk.Button(read_frame, text="Show Services Offered!", command=show_services).pack(pady=15)


# Wheaten Terrier at bottom
wheaten_terrier = Image.open("photos/wheaten-photo.jpg")
wheaten_terrier = wheaten_terrier.resize((400, 250))
photo_terrier = ImageTk.PhotoImage(wheaten_terrier)

wheaten_terrier = tk.Label(read_frame, image=photo_terrier)
wheaten_terrier.pack(pady=15)




# Update Tab
update_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(update_frame, text="Update your Info")











# Delete Tab
delete_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(delete_frame, text="Delete your Info")


tk.Label(
    delete_frame,
    text="Delete your Appointments, your Info & Pets Info!",
    font=('Comic Sans MS', 16, 'bold'),
    bg='lightblue'
).pack(pady=(10, 10))

info_columns = tk.Frame(delete_frame, bg='lightblue')
info_columns.pack(padx=20, pady=10)


# Appointment Info Entry Box
appt_frame = tk.LabelFrame(info_columns, text="Appointment Info", bg='lightblue', font=('Arial', 10, 'bold'))
appt_frame.grid(row=0, padx=10, pady=10)

tk.Label(appt_frame, text="Appointment ID", bg='lightblue').grid(row=0)
appt_id_delete_entry = tk.Entry(appt_frame)
appt_id_delete_entry.grid(row=1, pady=5)

tk.Label(appt_frame, text="First Name", bg='lightblue').grid(row=2)
fname_delete_entry = tk.Entry(appt_frame)
fname_delete_entry.grid(row=3, pady=5)

tk.Label(appt_frame, text="Last Name", bg='lightblue').grid(row=4)
lname_delete_entry = tk.Entry(appt_frame)
lname_delete_entry.grid(row=5, pady=5)


def delete_appointment():
    appt_id = appt_id_delete_entry.get()
    fname = fname_delete_entry.get().lower().strip()
    lname = lname_delete_entry.get().lower().strip()

    conn = sqlite3.connect("proj1.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT A.appointment_id
        FROM Appointments A
        JOIN Customers C ON A.customer_id = C.customer_id
        WHERE A.appointment_id = ? AND LOWER(C.first_name) = ? AND LOWER(C.last_name) = ?
    """, (appt_id, fname, lname))

    result = cursor.fetchone()

    if result:
        cursor.execute("""
            DELETE FROM Appointments
            WHERE appointment_id = ?
              AND customer_id = (
                  SELECT customer_id FROM Customers WHERE LOWER(first_name) = ? AND LOWER(last_name) = ?
              )
        """, (appt_id, fname, lname))

        conn.commit()
        messagebox.showinfo("Success!", "Your Appointment has been Deleted!")
    else:
        messagebox.showerror("Error", "Appointment does not exist or info is incorrect.")

    conn.close()

tk.Button(appt_frame, text="Delete Your Appointment!", command=delete_appointment).grid(row=6, pady=10)




# Pet Info Entry Box
pet_delete_frame = tk.LabelFrame(info_columns, text="Pet Info", bg='lightblue', font=('Arial', 10, 'bold'))
pet_delete_frame.grid(row=0, column=2, padx=10, pady=10)

tk.Label(pet_delete_frame, text="Pet ID", bg='lightblue').grid(row=0)
pet_id_delete_entry = tk.Entry(pet_delete_frame)
pet_id_delete_entry.grid(row=1, pady=5)

tk.Label(pet_delete_frame, text="Pet Name", bg='lightblue').grid(row=2)
pet_name_delete_entry = tk.Entry(pet_delete_frame)
pet_name_delete_entry.grid(row=3, pady=5)


def delete_pet_info():
    pet_delete_id = pet_id_delete_entry.get()
    pet_name_delete = pet_name_delete_entry.get().lower().strip()

    conn = sqlite3.connect("proj1.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Pets 
        WHERE pet_id = ? 
        AND LOWER(name) = ? 
    """, (pet_delete_id, pet_name_delete))

    result = cursor.fetchone()

    if result:
        cursor.execute("""
            DELETE FROM Pets 
            WHERE pet_id = ?
        """, (pet_delete_id))
        conn.commit()
        messagebox.showinfo("Success!", "Your Info has been Deleted!")
    else:
        messagebox.showerror("Error", "Pet does not exist or info is incorrect.")

    conn.close()

tk.Button(pet_delete_frame, text="Delete Your Pet Information!", command=delete_pet_info).grid(row=6, pady=10)



# Customer Info Entry Box
cust_delete_frame = tk.LabelFrame(info_columns, text="Customer Info", bg='lightblue', font=('Arial', 10, 'bold'))
cust_delete_frame.grid(row=0, column=3, padx=10, pady=10)

tk.Label(cust_delete_frame, text="Customer ID", bg='lightblue').grid(row=0)
customer_id_delete_entry = tk.Entry(cust_delete_frame)
customer_id_delete_entry.grid(row=1, pady=5)

tk.Label(cust_delete_frame, text="First Name", bg='lightblue').grid(row=2)
first_name_delete_entry = tk.Entry(cust_delete_frame)
first_name_delete_entry.grid(row=3, pady=5)

tk.Label(cust_delete_frame, text="Last Name", bg='lightblue').grid(row=4)
last_name_delete_entry = tk.Entry(cust_delete_frame)
last_name_delete_entry.grid(row=5, pady=5)


def delete_customer_info():
    customer_delete_id = customer_id_delete_entry.get()
    customer_fname_delete = first_name_delete_entry.get().lower().strip()
    customer_lname_delete = last_name_delete_entry.get().lower().strip()

    conn = sqlite3.connect("proj1.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Customers 
        WHERE customer_id = ? 
        AND LOWER(first_name) = ? 
        AND LOWER(last_name) = ?
    """, (customer_delete_id, customer_fname_delete, customer_lname_delete))

    result = cursor.fetchone()

    if result:
        cursor.execute("""
            DELETE FROM Customers 
            WHERE customer_id = ?
        """, (customer_delete_id,))
        conn.commit()
        messagebox.showinfo("Success!", "Your Info has been Deleted!")
    else:
        messagebox.showerror("Error", "Customer does not exist or info is incorrect.")

    conn.close()

tk.Button(cust_delete_frame, text="Delete Your Information!", command=delete_customer_info).grid(row=6, pady=10)


# Picture of Dog at bottom
doc_dog = Image.open("photos/doctor-photo.jpg")
doc_dog = doc_dog.resize((400, 250))
photo_doc = ImageTk.PhotoImage(doc_dog)

doc_dog = tk.Label(delete_frame, image=photo_doc)
doc_dog.pack(pady=15)


root.mainloop()
