import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import os
import subprocess

def open_main_application():
    subprocess.Popen(["python", "main.py"])

def validate_login(event=None):
    username = username_entry.get()
    password = password_entry.get()

    if not os.path.exists('user_data.csv'):
        create_user_data_file()

    try:
        with open('user_data.csv', 'r') as file:
            if os.stat('user_data.csv').st_size == 0:
                messagebox.showwarning("No Registrations", "Please register first")
                return

            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                    clear_entries()
                    open_main_application()
                    return
        messagebox.showerror("Login Failed", "Invalid username or password")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def register(event=None):
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()

    if not os.path.exists('user_data.csv'):
        create_user_data_file()

    try:
        with open('user_data.csv', 'r') as file:
            reader = csv.reader(file)
            if os.stat('user_data.csv').st_size > 0:
                messagebox.showerror("Registration Failed", "1 user is already registered. This Login Page is restricted to 1 user only, so only 1 user can register")
                return

        with open('user_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([new_username, new_password])

        messagebox.showinfo("Registration Successful", "You have been registered successfully!")
        clear_entries()
        update_registration_count()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def update_registration_count():
    try:
        if os.path.exists('user_data.csv'):
            with open('user_data.csv', 'r') as file:
                reader = csv.reader(file)
                registration_count = sum(1 for row in reader)
                registration_count_label.config(text="Number of Registrations: {}".format(registration_count))
        else:
            registration_count_label.config(text="Number of Registrations: 0")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clear_entries():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    new_username_entry.delete(0, tk.END)
    new_password_entry.delete(0, tk.END)

def create_user_data_file():
    try:
        with open('user_data.csv', 'w', newline=''):
            pass
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Login and Registration System")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Load background image and resize it to fit the screen
background_image = Image.open("background_image.png")
image_width, image_height = background_image.size
ratio = min(screen_width/image_width, screen_height/image_height)
background_image = background_image.resize((int(image_width * ratio), int(image_height * ratio)), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label with the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create labels and entries for username and password
username_label = tk.Label(root, text="Username:", bg="white")
username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=10, pady=5)
username_entry.bind('<Return>', lambda event: password_entry.focus())

password_label = tk.Label(root, text="Password:", bg="white")
password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)
password_entry.bind('<Return>', validate_login)

# Create login button
login_button = tk.Button(root, text="Login", command=validate_login, bg="#4CAF50", fg="white")
login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Create labels and entries for new registration
new_username_label = tk.Label(root, text="New Username:", bg="white")
new_username_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

new_username_entry = tk.Entry(root)
new_username_entry.grid(row=4, column=1, padx=10, pady=5)
new_username_entry.bind('<Return>', lambda event: new_password_entry.focus())

new_password_label = tk.Label(root, text="New Password:", bg="white")
new_password_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")

new_password_entry = tk.Entry(root, show="*")
new_password_entry.grid(row=5, column=1, padx=10, pady=5)
new_password_entry.bind('<Return>', register)

# Create register button
register_button = tk.Button(root, text="Register", command=register, bg="#008CBA", fg="white")
register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Label to display registration count
registration_count_label = tk.Label(root, text="Number of Registrations: 0", bg="white")
registration_count_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# Update registration count initially
update_registration_count()

root.mainloop()