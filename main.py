import string
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    s1 = list(string.ascii_lowercase)
    s2 = list(string.ascii_uppercase)
    s3 = list(string.digits)
    s4 = list(string.punctuation)

    random.shuffle(s1)
    random.shuffle(s2)
    random.shuffle(s3)
    random.shuffle(s4)

    part1 = round(10 * (30/100))
    part2 = round(10 * (20/100))

    result = []

    for x in range(part1):
        result.append(s1[x])
        result.append(s2[x])

    for x in range(part2):
        result.append(s3[x])
        result.append(s4[x])

    random.shuffle(result)

    random_password = "".join(result)
    pyperclip.copy(random_password)
    password_text.delete(0, END)
    password_text.insert(0, random_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = text_field_website.get()
    email_username = username_text.get()
    password = password_text.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Dont leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as my_file:
                #Reading old data
                data = json.load(my_file)
        except FileNotFoundError:
            with open("data.json", "w") as my_file:
                json.dump(new_data, my_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as my_file:
                #Saving updated data
                json.dump(data, my_file, indent=4)
        finally:
            text_field_website.delete(0, END)
            password_text.delete(0, END)
# ---------------------------- SEARCH --------------------------------- #
def find_password():
    website = text_field_website.get()
    try:
        with open("data.json", "r") as my_file:
            # Reading old data
            data = json.load(my_file)
            saved_password = data[website]
    except FileNotFoundError:
        messagebox.showwarning(title="Oops", message="Empty list")
    except KeyError:
        messagebox.showwarning(title="Oops", message="No details for the website exists")
    else:
        messagebox.showinfo(message=f"Website: {website} \n"
                                    f"Email: {saved_password['email']} \n"
                                    f"Password: {saved_password['password']}")
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
img_mypass = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img_mypass)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.config(font=(FONT_NAME, 15, "bold"))
website_label.grid(row=1, column=0)

text_field_website = Entry(width=42, )
text_field_website.grid(row=1, column=1)

username_label = Label(text="Email/Username:")
username_label.config(font=(FONT_NAME, 15, "bold"))
username_label.grid(row=2, column=0)

username_text = Entry(width=61, )
username_text.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:")
password_label.config(font=(FONT_NAME, 15, "bold"))
password_label.grid(row=3, column=0)

password_text = Entry(width=42, )
password_text.grid(row=3, column=1)

generate_pass = Button(text="Generate Password")
generate_pass.config(command=generate_password)
generate_pass.grid(row=3, column=2)

add_button = Button(text="Add")
add_button.config(width=52, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search")
search_button.config(width=15, command=find_password)
search_button.grid(row=1, column=2)




window.mainloop()
