from tkinter import *
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
from tkinter import messagebox

key = Fernet.generate_key()
user_credentials = {}


def save_encrypt():
    title = title_entry.get()
    text = secret_text.get("1.0", END)
    password = pswd_entry.get()
    if not title or not text or not password:
        messagebox.showerror("Error", "Title,text and password must be given.")
        return

    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode())
    try:
        with open('my_secrets.txt', 'a') as file:
            file.write(title)
            file.write("\n")
        with open('my_secrets.txt', 'ab') as file:
            file.write(encrypted_text)
        with open('my_secrets.txt', 'a') as file:
            file.write("\n")
    except FileNotFoundError:
        with open('my_secrets.txt', 'w') as file:
            file.write(title)
            file.write("\n")
        with open('my_secrets.txt', 'ab') as file:
            file.write(encrypted_text)
        with open('my_secrets.txt', 'a') as file:
            file.write("\n")

    user_credentials[title]=password


def decrypt():
    entered_password = pswd_entry.get()
    title = title_entry.get()
    if title in user_credentials:
        if user_credentials[title] == entered_password:
            text = secret_text.get("1.0", END)
            cipher_suite = Fernet(key)
            decrypted_text = cipher_suite.decrypt(text.encode())
            decrypted_text_str = decrypted_text.decode()
            secret_text.delete("1.0", END)
            secret_text.insert(END, decrypted_text_str)
        else:
            messagebox.showerror("Error", "Password is incorrect.")
    else:
        messagebox.showerror("Error", "Note not found.")


window=Tk()
window.title("Secret Notes")
window.geometry("650x750")
window.config(padx=40,pady=40)

image_path = "./images/secret_stamp.jpg"
img = Image.open(image_path)
img = img.resize((150, 150), Image.LANCZOS)
stamp = ImageTk.PhotoImage(img)


image_label = Label(image=stamp)
image_label.pack(padx=10, pady=10)
title_label=Label(text="Enter your title",font=("bold",16))
title_label.pack()
title_entry=Entry()
title_entry.pack()
secret_label=Label(text="Enter your secret",font=("bold",16))
secret_label.pack()
secret_text=Text(width=50,height=15)
secret_text.pack()
pswd_label=Label(text="Enter your password",font=("bold",16))
pswd_label.pack()
pswd_entry=Entry(width=30)
pswd_entry.pack()
save_enc_button=Button(text="Save & Encrypt",command=save_encrypt)
save_enc_button.pack()
decrypt_button=Button(text="Decrypt",command=decrypt)
decrypt_button.pack()

window.mainloop()