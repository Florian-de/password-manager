from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_passwort():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website.title(): {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n {website} | {email} | {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open(file="data.json", mode='r') as json_file:
                    data = json.load(json_file)
                    data.update(new_data)
            except FileNotFoundError:
                data = new_data

            with open(file="data.json", mode='w') as file:
                json.dump(data, file, indent=4)
                website_entry.delete(0, END)
                password_entry.delete(0, END)

def search_website():
    searched_website = website_entry.get()
    try:
        with open(file="data.json", mode='r') as file:
            website_data = json.load(file)[searched_website.title()]
            #Clean entrys
            email_entry.delete(0, END)
            password_entry.delete(0, END)
            #Set entrys with searched data
            email_entry.insert(0, website_data["email"])
            password_entry.insert(0, website_data["password"])
    except FileNotFoundError:
        messagebox.showinfo(title="No Data", message="No Data available")
    except KeyError:
        messagebox.showinfo(title="No Data", message="No Data available")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Passwort Manager")
window.config(pady=40, padx=40, bg="white")

canvas = Canvas(width=200, height=200, bg="white")

website_label = Label(text="Website:", bg="white", highlightthickness=0, fg="black")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", bg="white", highlightthickness=0, fg="black")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", bg="white", highlightthickness=0, fg="black")
password_label.grid(row=3, column=0)

website_entry = Entry(width=21, bg="white", fg="black", highlightthickness=0)
website_entry.grid(row=1, column=1, pady=2)
website_entry.focus()
email_entry = Entry(width=37, bg="white", fg="black", highlightthickness=0)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "flori.dreyer@gmail.com")
password_entry = Entry(width=21, bg="white", fg="black", highlightthickness=0)
password_entry.grid(row=3, column=1)

password_button = Button(text="Generate Password", bg="white", fg="black", highlightthickness=0, width=11, highlightbackground="white", command=generate_password)
password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, bg="white", fg="black", highlightthickness=0, highlightbackground="white", command=save_passwort)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", bg="white", fg="black", highlightthickness=0, width=11, highlightbackground="white", command=search_website)
search_button.grid(row=1, column=2, pady=3)





logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.config(highlightthickness=0)
canvas.grid(row=0, column=1)

window.mainloop()