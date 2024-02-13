import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps 
from tkinter import messagebox

# messagebox.showinfo("Hello", "Hello")

db_connection = sqlite3.connect("contacts.db") # Create database file if not exists and connecting to the database.
db_cursor = db_connection.cursor()
db_cursor.execute("CREATE TABLE if not exists list(id int, name text, number int, email text, address text)") # Create "tasks" named table if not exists.
table_data = db_cursor.execute("select * from list").fetchall()
# print(*table_data)

root = Tk()
root.title("Contact Book")
root.geometry("780x600+400+200")
root.resizable(0, 0)
root.config(bg="#fff")

def add_dialog(index_id=-1, name="", number="", email="", address=""):
    add_window = Toplevel(root)
    add_window.config(bg="#fff")
    add_window.geometry("320x400+440+370")
    add_window.title("Add Contact")
    # add_window.focus_force()
    add_window.resizable(0, 0)
    # add_window.attributes('-toolwindow', True)
    add_window.grab_set()

    Label(add_window, image=images[4], bg="#fff").pack(pady=10)

    main_frame = Frame(add_window, bg="#fff")
    main_frame.pack()

    entry_frm1 = Frame(main_frame, width=250, height=35, bg="#fff", highlightthickness=1, highlightbackground="#303030", highlightcolor="#52b1ff")
    entry_frm2 = Frame(main_frame, width=250, height=35, bg="#fff", highlightthickness=1, highlightbackground="#303030", highlightcolor="#52b1ff")
    entry_frm3 = Frame(main_frame, width=250, height=35, bg="#fff", highlightthickness=1, highlightbackground="#303030", highlightcolor="#52b1ff")
    entry_frm4 = Frame(main_frame, width=250, height=35, bg="#fff", highlightthickness=1, highlightbackground="#303030", highlightcolor="#52b1ff")
    entry_frm1.pack(pady=10)
    entry_frm2.pack(pady=10)
    entry_frm3.pack(pady=10)
    entry_frm4.pack(pady=10)

    def on_focus(event, word):
        global pword
        pword = word
        widget = event.widget

        if widget.get() == word:
            widget.delete(0, END)
        widget.config(fg="#1f1f1f")

    def on_leave(event):
        word = pword
        widget = event.widget

        if not widget.get():
            widget.insert(0, word)
            widget.config(fg="#808080")

    def save_data():
        name = name_entry.get()
        number = number_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        allVar = False

        for var, placeholder in zip([name, number, email, address], [name_placeholder, number_placeholder, email_placeholder, address_placeholder]):
            if not var == placeholder and var:
                allVar = True
            else:
                allVar = False

        if allVar:
            index = contact_list.index(END)
            # print(index)
            if index_id >= 0:
                contact_list.delete(index_id)
                contact_list.insert(index_id, name)
                db_cursor.execute("update list set (id, name, number, email, address) = (?, ?, ?, ?, ?) where id = (?)", (index_id, name, number, email, address, index_id))
                contact_name.config(text=name)
                contact_number.config(text=number)
                contact_email.config(text=email)
                contact_address.config(text=address)
            else:
                contact_list.insert(END, name)
                db_cursor.execute('insert into list (id, name, number, email, address) values (?, ?, ?, ?, ?)', (index, name, number, email, address))  # inserting contact details to the list table in database.
            db_connection.commit()

    name_lbl = Label(main_frame, text="Name", bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))
    number_lbl = Label(main_frame, text="Number", bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))
    email_lbl = Label(main_frame, text="Email", bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))
    address_lbl = Label(main_frame, text="Address", bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))

    name_lbl.place(x=5, y=2)
    number_lbl.place(x=5, y=57)
    email_lbl.place(x=5, y=112)
    address_lbl.place(x=5, y=167)

    name_entry = Entry(entry_frm1, fg="#808080", width=29, font=("Arial", 11), borderwidth=0)
    number_entry = Entry(entry_frm2, fg="#808080", width=29, font=("Arial", 11), borderwidth=0)
    email_entry = Entry(entry_frm3, fg="#808080", width=29, font=("Arial", 11), borderwidth=0)
    address_entry = Entry(entry_frm4, fg="#808080", width=29, font=("Arial", 11), borderwidth=0)

    name_placeholder = "Full Name"
    number_placeholder = "Number"
    email_placeholder = "Email"
    address_placeholder = "Address"

    for _widget, placeholder in zip([name_entry, number_entry, email_entry, address_entry], [name_placeholder, number_placeholder, email_placeholder, address_placeholder]):
        _widget.place(x=7, y=6)
        _widget.bind("<FocusIn>", lambda e, p=placeholder: on_focus(e, p))
        _widget.bind("<FocusOut>", on_leave)
        _widget.insert(0, placeholder)

    if any(var for var in [name, number, email, address]):
        for widget_, text in zip([name_entry, number_entry, email_entry, address_entry], [name, number, email, address]):
            widget_.config(fg="#1f1f1f")
            widget_.delete(0, END)
            widget_.insert(0, text)

    name_entry.focus_force()

    button_frame = Frame(
        add_window,
        bg="#fff"
        )
    button_frame.pack(fill=X)

    save_btn = Button(button_frame, image=images[3], bg="#77C2FF", activebackground="#5cb3fb", pady=5, width=245, height=30, borderwidth=0, font=("Verdana", 10), command=save_data)
    save_btn.pack(pady=8)
    save_btn.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))
    save_btn.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))

def update_list():
    list_data = [row[0] for row in db_cursor.execute('SELECT name FROM list')]
    contact_list.insert(END, *list_data)

def update_dialog():
    index = contact_list.curselection()[0]
    data = db_cursor.execute('SELECT * FROM list WHERE id = ?', (index,)).fetchone()
    id_, name, number, email, address = data

    add_dialog(
        index_id=id_,
        name=name,
        number=number,
        email=email,
        address=address
        )

def delete_contact():
    try:
        index = contact_list.curselection()[0]
        db_cursor.execute("delete from list where id = ?", (index,))
        contact_list.delete(index)
        db_connection.commit()
        getpass = True
    except Exception:
        getpass = False

    if getpass:
        contacts = contact_list.get(0, END)
        data = db_cursor.execute('SELECT * FROM list').fetchall()
        ids = [row[0] for row in data]

        for index, contact in enumerate(contacts):
            db_cursor.execute("update list set id = ? where id = ?", (index, ids[index]))
    db_connection.commit()

image_path = [
    "images/plus.png",
    "images/edit.png",
    "images/trash.png",
    "images/save.png",
    "images/profile.png",
    "images/phone-v2.png",
    "images/email-v2.png",
    "images/location-v2.png"
    ]

image_coordinates = [
    (20, 20),
    (20, 20),
    (18, 20),
    (18, 20),
    (102, 100),
    (18, 20),
    (18, 18),
    (16, 20)
]
images = []

for index, image in enumerate(image_path):
    x, y = image_coordinates[index]
    image = Image.open(image).resize((x, y))
        # Separate the image into channels (R, G, B, A)
    r, g, b, a = image.split()

    # Invert the RGB channels
    r = Image.eval(r, lambda x: 255)
    g = Image.eval(g, lambda x: 255)
    b = Image.eval(b, lambda x: 255)

    # Combine the inverted RGB channels with the original alpha channel
    inverted_img = Image.merge('RGBA', (r, g, b, a))
    if index >= 4:
        images.append(ImageTk.PhotoImage(image))
    else:
        images.append(ImageTk.PhotoImage(inverted_img))

detail_frame = Frame(root, bg="#fff", width=360, height=560, highlightbackground="#808080", highlightthickness=2)
detail_frame.place(x=400, y=20)

Label(detail_frame, image=images[4], bg="#fff").place(x=120, y=30)

contact_name = Label(
    detail_frame,
    font=("Arial", 15, "bold"),
    justify="center",
    width=24,
    bg="#fff"
    )
contact_name.place(x=30, y=145)

contact_info = Frame(
    detail_frame,
    borderwidth=2,
    relief="ridge",
    width=325, height=180, bg="#fff",
    )

Label(
    contact_info,
    bg="#fff",
    text="Contact info",
    font=("Arial", 12, "bold")
    ).place(x=8, y=10)

contact_number = Label(
    contact_info,
    image=images[5],
    compound="left",
    font=("Roboto", 12),
    anchor="w",
    width=290,
    padx=10,
    bg="#fff"
    )
contact_number.place(x=0, y=50)

contact_email = Label(
    contact_info,
    image=images[6],
    compound="left",
    font=("Roboto", 12),
    anchor="w",
    width=290,
    padx=10,
    bg="#fff"
    )
contact_email.place(x=0, y=80)

contact_address = Label(
    contact_info,
    image=images[7],
    compound="left",
    font=("Roboto", 12),
    anchor="w",
    width=290,
    padx=10,
    bg="#fff"
    )
contact_address.place(x=0, y=110)

frame_line1 = Frame(detail_frame, height=4, width=160, bg="#808080")
frame_line2 = Frame(detail_frame, height=4, width=280, bg="#808080")
frame_line3 = Frame(detail_frame, height=4, width=280, bg="#808080")
frame_line4 = Frame(detail_frame, height=4, width=280, bg="#808080")
frame_line5 = Frame(detail_frame, height=4, width=280, bg="#808080")

frame_line1.place(x=95, y=160)
frame_line2.place(x=35, y=240)
frame_line3.place(x=35, y=320)
frame_line4.place(x=35, y=400)
frame_line5.place(x=35, y=480)

contact_frame = Frame(root, bg="#fff", width=360, height=560, highlightbackground="#808080", highlightthickness=2)
contact_frame.place(x=20, y=20)

search_frame = Frame(contact_frame, bg="#fff")
search_frame.place(x=14, y=15)

search_border = Frame(search_frame, width=227, borderwidth=0, height=35, bg="#fff", highlightthickness=2, highlightbackground="#808080", highlightcolor="#52b1ff")
search_border.pack(side="left", padx=6)

search_value = StringVar()
search_box = Entry(search_border, textvariable=search_value, fg="#505050", width=27, font=("Arial", 11), borderwidth=0)
search_box.place(x=5, y=6)
search_placeholder = "Search contacts"
search_box.insert(0, search_placeholder)

# contact_name.config(textvariable=search_value)

search_box.bind("<FocusIn>", lambda event : event.widget.delete(0, END))
search_box.bind("<FocusOut>", lambda event : event.widget.insert(0, search_placeholder))

search_btn = Button(search_frame, fg="#fff", text="Search", width=8, height=1, relief="ridge", borderwidth=2, bg="#77C2FF", activebackground="#5cb3fb", activeforeground="#fff", pady=4, font=("Arial", 11))
search_btn.pack(side="left")
search_btn.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))
search_btn.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))

# lsbox_frame = Frame(main_frame, highlightbackground="#77C2FF", highlightthickness=1)
# lsbox_frame.place(x=8, y=70)

def show_contact(event):
    widget = event.widget
    try:
        index = widget.curselection()[0]
        value = widget.get(index)
        getpass = True
        contact_name.config(text=value)
    except Exception:
        getpass = False

    if getpass:
        contact_info.place(x=15, y=200)
        frame_line1.place_forget()
        frame_line2.place_forget()
        frame_line3.place_forget()
        frame_line4.place_forget()
        frame_line5.place_forget()
        # print(index)
        data = db_cursor.execute('SELECT * FROM list WHERE id = ?', (index,)).fetchone()
        id_, name, number, email, address = data
        # print(id_, name, number, email, address)
        contact_number.config(text=number)
        contact_email.config(text=email)
        contact_address.config(text=address)

contact_list = Listbox(
    contact_frame,
    borderwidth=0,
    justify="center",
    activestyle="none",
    height=22, width=39,
    selectbackground="#77C2FF",
    selectforeground="#101010",
    highlightbackground="#808080",
    highlightthickness=2,
    highlightcolor="#52b1ff",
    font=("Roboto", 11)
    )

contact_list.place(x=20, y=65)
contact_list.bind("<<ListboxSelect>>", show_contact)

update_list()

button_frame = Frame(
    contact_frame, width=315, height=45,
    bg="#fff",
    # borderwidth=1, relief="solid"
    )
# button_frame.pack(fill=X, side="bottom", pady=10)
button_frame.place(x=20, y=500)

btn_text = ["Add", "Update", "Delete"]

add_btn = Button(button_frame, command=add_dialog, width=70)
update_btn = Button(button_frame, command=update_dialog, width=70)
delete_btn = Button(button_frame, command=delete_contact, width=70)

add_btn.place(x=0, y=0)
update_btn.place(x=109, y=0)
delete_btn.place(x=219, y=0)

for index, widget in enumerate([add_btn, update_btn, delete_btn]):
    widget.config(
        text=btn_text[index],
        font=("Arial", 12),
        bg="#77C2FF",
        fg="#fff",
        activeforeground="#fff",
        activebackground="#77C2FF",
        borderwidth=2,
        relief="ridge",
        image=images[index], compound="left",
        height=35,
        padx=10,
        )
    widget.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))
    widget.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))

root.mainloop()
