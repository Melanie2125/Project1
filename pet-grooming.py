import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()

root.geometry("765x800")
root.title("Pet Grooming Shop Management System")
root.configure(bg='lightblue')

style = ttk.Style()

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)
style.configure('TNotebook.Tab', font=('Comic Sans MS', 11))

style.configure('TNotebook.Tab',
                background='yellow',
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

image_pet_grooming = Image.open("pet-photo.jpg")
image_pet_grooming = image_pet_grooming.resize((300, 150))
photo_pet_grooming = ImageTk.PhotoImage(image_pet_grooming)

image_grooming = tk.Label(home_frame, image=photo_pet_grooming, bg='#f9f9f9')
image_grooming.pack(pady=(0, 20))

features_text = (
    "•  Create new appointments, add pets, and enter your customer information.\n"
    "•  Review your appointments, personal details, pet profiles, and available services.\n"
    "•  Update your information, pet details, or modify existing appointments.\n"
    "•  Delete your account, pets, or appointments if needed."
)

features_label = tk.Label(home_frame, text=features_text, font=('Comic Sans MS', 12), justify='left', bg='lightblue')
features_label.pack(padx=20, pady=10)

image_dog = Image.open("dog-photo.jpg")
image_dog = image_dog.resize((300, 150))
photo_dog = ImageTk.PhotoImage(image_dog)

image_dog = tk.Label(home_frame, image=photo_dog, bg='#f9f9f9')
image_dog.pack(pady=(0, 20))

# Create Tab
create_frame = tk.Frame(notebook, bg='lightblue')
notebook.add(create_frame, text="Create Appointment & Info")

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
