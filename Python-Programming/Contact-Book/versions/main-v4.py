import re
import pickle
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

def add_dialog(index_id=-1, title="", number="", email="", address=""):
    add_window = Toplevel(root)
    add_window.config(bg="#fff")
    add_window.geometry("320x400+440+370")
    add_window.title("Add Contact")
    # add_window.focus_force()
    add_window.resizable(0, 0)
    # add_window.attributes('-toolwindow', True)
    add_window.grab_set()

    # def alert_box(title, message):
        # alert_window = Toplevel(add_window)
        # alert_window.geometry("250x150+300+200")
        # alert_window.title(title)
        # alert_window.grab_set()
        # Label(alert_window, text=message, font=("Arial", 11)).pack(anchor="center", padx=20, pady=20)
        # Button(alert_window, text="OK", width=10, border=0, bg="#fff").pack(side="bottom", pady=10)

    Label(add_window, image=images[1], bg="#fff").pack(pady=10)

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

    entry_exceptions = [
        "Name or number field required!",
        "This field required number!",
        "Name limits to 25 characters!",
        "Number limits to 20 numbers!",
        "Email limits to 63 characters!",
        "The email address is invalid!",
        "Address limits to 100 characters!"
        ]

    def on_focus(event, word):
        global pword
        pword = word
        widget = event.widget

        if number_entry.get() == entry_exceptions[3]:
            number_entry.delete(0, END)
            number_entry.config(fg="#808080")
            number_entry.insert(0, number_placeholder)

        if widget.get() == word or widget.get() in entry_exceptions:
            widget.delete(0, END)
        widget.config(fg="#1f1f1f")

    def on_leave(event):
        word = pword
        widget = event.widget

        if not widget.get():
            widget.insert(0, word)
            widget.config(fg="#808080")

    titlelen = BooleanVar()
    numberlen = BooleanVar()
    isnumber = BooleanVar()
    emaillen = BooleanVar()
    isemail = BooleanVar()
    addresslen = BooleanVar()

    def save_data():
        name = split_character(name_entry.get())
        number = number_entry.get()
        email = split_character(email_entry.get())
        address = split_character(address_entry.get())

        title = ""
        _number = ""
        _email = ""
        _address = ""

        variables = {
            "name":name,
            "number":number,
            "email":email,
            "address":address
        }

        empty_variables = [
            key for key, value in variables.items()
            if value in [name_placeholder, number_placeholder, email_placeholder, address_placeholder] or not value
            ]

        # print(empty_variables)
        field = False

        if "name" in empty_variables and "number" in empty_variables:
            messagebox.showwarning("Add contact", entry_exceptions[0], parent=add_window)
            add_window.focus_force()

        if not "name" in empty_variables and not "number" in empty_variables:
            title = name
            _number = number
            if isnumber.get():
                field = True
            else:
                field = False
        
        elif not "name" in empty_variables:
            title = name
            field = True

        elif not "number" in empty_variables:
            title = number
            _number = number
            if isnumber.get():
                field = True
            else:
                field = False

        if not "email" in empty_variables:
            _email = email
            validate_email(widget=email_entry)
            if isemail.get():
                field = True
            else:
                field = False

        if not "address" in empty_variables:
            _address = address

        # print(f"titlelen: {titlelen.get()}\nnumberlen: {numberlen.get()}\nisnumber: {isnumber.get()}\nemaillen: {emaillen.get()}\nisemail: {isemail.get()}\naddresslen: {addresslen.get()}")
        # print(f"title: {title}\nnumber: {_number}\nemail: {_email}\naddress: {_address}")

        if field:
            index = contact_list.index(END)
            # print(index)
            if index_id >= 0:
                index = index_id
                contact_list.delete(index_id)
                contact_list.insert(index_id, title)
                db_cursor.execute("update list set (name, number, email, address) = (?, ?, ?, ?) where id = (?)", (title, _number, _email, _address, index_id))

                contact_title.config(text=title)

                if _number:
                    contact_number.config(text=_number)
                else:
                    contact_number.config(text="Add phone number")

                if _email:
                    contact_email.config(text=_email)
                else:
                    contact_email.config(text="Add email")
                    
                if _address:
                    contact_address.config(text=_address)
                else:
                    contact_address.config(text="Add Address")
            else:
                contact_list.insert(END, title)
                db_cursor.execute('insert into list (id, name, number, email, address) values (?, ?, ?, ?, ?)', (index, title, _number, _email, _address))  # inserting contact details to the list table in database.
            # contact_list.select_set(index)
            show_contact(event=contact_list, getindex=index)
            db_connection.commit()
            add_window.destroy()
            change_frame()

    name_lbl = Label(main_frame, text="Name", bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))
    number_lbl = Label(main_frame, text="Number", bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))
    email_lbl = Label(main_frame, text="Email", bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))
    address_lbl = Label(main_frame, text="Address", bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))

    name_lbl.place(x=5, y=2)
    number_lbl.place(x=5, y=57)
    email_lbl.place(x=5, y=112)
    address_lbl.place(x=5, y=167)

    def config_entry( widget, value=None, count=0):
        widget.config(fg="#1f1f1f")
        widget.delete(0, END)

        if value:
            if value in placeholders:
                widget.config(fg="#808080")
                widget.insert(0, value)
            else:
                widget.insert(0, value[0:count])

    def validate_name(*args):
        name = name_value.get()

        if not name == "Full Name":
            if len(name) > 25:
                titlelen.set(False)
                tmpValue = name
                name_entry.config(fg="#ff6969")
                name_value.set(entry_exceptions[2])
                name_entry.after(1000, config_entry, name_entry, tmpValue, 25)
                add_window.focus_force()
            else:
                if len(name) > 0:
                    titlelen.set(True)
        else:
            titlelen.set(False)

    def validate_number(*args):
        number = number_value.get()

        if not number == "Number":
            if len(number) > 20:
                numberlen.set(False)
                if not number == entry_exceptions[3]:
                    tmpValue = number
                    number_entry.config(fg="#ff6969")
                    number_value.set(entry_exceptions[3])
                    number_entry.after(1000, config_entry, number_entry, tmpValue, 20)
                    add_window.focus_force()
            else:
                if len(number) > 0:
                    numberlen.set(True)
                if number.isdigit():
                    isnumber.set(True)
                    number_entry.config(fg="#1f1f1f")
                    number_value.set(number)
                else:
                    isnumber.set(False)
                    # number_value.set("")
                    if number.isalpha():
                        number_entry.config(fg="#ff6969")
                        number_value.set(entry_exceptions[1])
                        number_entry.after(1000, config_entry, number_entry, "Number")
                        add_window.focus_force()
        else:
            numberlen.set(False)

    def validate_email(widget=None, *args):
        email = email_value.get()

        try:
            widget.get()
            # Regular expression pattern for validating email addresses
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
            # Use re.match to search the pattern in the given email
            if not re.match(pattern, email):
                if not email == "Email" and email:
                    isemail.set(False)
                    tmpValue = email
                    email_entry.config(fg="#ff6969")
                    email_value.set(entry_exceptions[5])
                    address_entry.after(1000, config_entry, email_entry, tmpValue, len(tmpValue))
                    add_window.focus_force()
                else:
                    emaillen.set(False)
            else:
                isemail.set(True)

        except Exception:

            if not email == "Email":
                if len(email) > 63:
                    emaillen.set(False)
                    tmpValue = email
                    email_entry.config(fg="#ff6969")
                    email_value.set(entry_exceptions[4])
                    address_entry.after(1000, config_entry, email_entry, tmpValue, 63)
                    add_window.focus_force()
                else:
                    if len(email) > 0:
                        emaillen.set(True)
            else:
                emaillen.set(False)

    def validate_address(*args):
        address = address_value.get()

        if not address == "Address":
            if len(address) > 100:
                addresslen.set(False)
                tmpValue = address
                address_entry.config(fg="#ff6969")
                address_value.set(entry_exceptions[6])
                address_entry.after(1000, config_entry, address_entry, tmpValue, 100)
                add_window.focus_force()
            else:
                if len(address) > 0:
                    addresslen.set(True)
        else:
            addresslen.set(False)

    number_value = StringVar()
    number_value.trace_add(mode="write", callback=validate_number)

    name_value = StringVar()
    name_value.trace_add(mode="write", callback=validate_name)

    email_value = StringVar()
    email_value.trace_add(mode="write", callback=validate_email)

    address_value = StringVar()
    address_value.trace_add(mode="write", callback=validate_address)

    name_entry = Entry(entry_frm1, textvariable=name_value, fg="#808080", width=29, font=("Arial", 11), borderwidth=0)
    number_entry = Entry(entry_frm2, textvariable=number_value, fg="#808080", width=29, font=("Arial", 11), borderwidth=0)
    email_entry = Entry(entry_frm3, textvariable=email_value, fg="#808080", width=29, font=("Arial", 11), borderwidth=0)
    address_entry = Entry(entry_frm4, textvariable=address_value, fg="#808080", width=29, font=("Arial", 11), borderwidth=0)

    name_placeholder = "Full Name"
    number_placeholder = "Number"
    email_placeholder = "Email"
    address_placeholder = "Address"
    
    entries = [name_entry, number_entry, email_entry, address_entry]
    placeholders = [name_placeholder, number_placeholder, email_placeholder, address_placeholder]

    for _widget, placeholder in zip(entries, placeholders):
        _widget.place(x=7, y=6)
        _widget.bind("<FocusIn>", lambda e, p=placeholder: on_focus(e, p))
        _widget.bind("<FocusOut>", on_leave)
        _widget.insert(0, placeholder)

    if any(var for var in [title, number, email, address]):
        for widget_, placeholder, text in zip(entries, placeholders, [title, number, email, address]):
            if text == str(number):
                continue
            elif text:
                widget_.config(fg="#1f1f1f")
                widget_.delete(0, END)
                widget_.insert(0, text)

    name_entry.focus_force()

    button_frame = Frame(
        add_window,
        bg="#fff"
        )
    button_frame.pack(fill=X)

    save_btn = Button(button_frame, image=images[6], bg="#77C2FF", activebackground="#5cb3fb", pady=5, width=245, height=30, borderwidth=0, font=("Verdana", 10), command=save_data)
    save_btn.pack(pady=8)
    save_btn.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))
    save_btn.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))
    add_window.bind("<Return>", lambda e : save_data())

def change_frame():
    if contact_list.size() == 0:
        contact_list.place_forget()
        empty_contact.place(x=0, y=100)
    else:
        empty_contact.place_forget()
        contact_list.place(x=0, y=40)

def split_character(string):
    if "\n" in string:
        string = string.replace("\n", "")

    if len(string) > 24:
        output_string = ""
        for i in range(0, len(string), 24):
            output_string += string[i:i+24] + '\n'
        # print(output_string)
        return output_string
    return string

def update_list(*args):
    # hide_contact(None)
    list_data = [row[0] for row in db_cursor.execute('SELECT name FROM list')]

    contact_list.delete(0, END)

    search_term = search_value.get()

    if search_term == "" or search_term == search_placeholder:
        for item in list_data:
            contact_list.insert(END, item)
    else:
        for item in list_data:
            if search_term.lower() in item.lower():
                contact_list.insert(END, item)
    change_frame()

def update_dialog():
    getpass = False

    try:
        index = contact_list.curselection()
        if len(index) > 1:
            messagebox.showinfo("Update contact", "Select a contact to update!")
        elif len(index) > 0 and len(index) <= 1:
            getpass = True
        else:
            raise IndexError()

    except Exception:
        messagebox.showinfo("Update contact", "No contact selected!")

    if getpass:
        data = db_cursor.execute('SELECT * FROM list WHERE id = ?', (index[0],)).fetchone()
        id_, name, number, email, address = data

        add_dialog(
            index_id=id_,
            title=name,
            number=number,
            email=email,
            address=address
            )

def delete_contact():

    try:
        selected_index = contact_list.curselection()
        if not selected_index:
            raise IndexError()
        if len(selected_index) > 1:
            words = f"{len(selected_index)} contacts"
        else:
            words = "This contact"
        getpass = messagebox.askquestion(f"Delete {words.split()[-1]}", f"{words} will be deleted.\nAre you sure ?")
    except Exception:
        getpass = False
        messagebox.showinfo("Delete contact", "No contact selected!")

    if getpass == "yes":
        frame_line1.place(x=95, y=160)
        frame_line2.place(x=35, y=240)
        frame_line3.place(x=35, y=320)
        frame_line4.place(x=35, y=400)
        frame_line5.place(x=35, y=480)
        title_frame.place_forget()
        contact_info.place_forget()

        for index in reversed(selected_index):
            db_cursor.execute("delete from list where id = ?", (index,))
            contact_list.delete(index)
        db_connection.commit()

        contacts = contact_list.get(0, END)
        data = db_cursor.execute('SELECT * FROM list').fetchall()
        ids = [row[0] for row in data]

        # print(contacts)
        # print(ids)

        for index, contact in enumerate(contacts):
            pass
            db_cursor.execute("update list set id = ? where id = ?", (index, ids[index]))
    db_connection.commit()
    change_frame()

image_path = [
    "images/background.png",
    "images/profile.png",
    "images/search.png",
    "images/plus.png",
    "images/edit.png",
    "images/trash.png",
    "images/save.png",
    "images/phone-v2.png",
    "images/email-v2.png",
    "images/location-v2.png",
    ]

image_coordinates = [
    (345, 240),
    (102, 100),
    (20, 20),
    (20, 20),
    (20, 20),
    (18, 20),
    (18, 20),
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
    if index <= 1 or index >= 7:
        images.append(ImageTk.PhotoImage(image))
        # images.append(image)
    else:
        images.append(ImageTk.PhotoImage(inverted_img))
        # images.append(inverted_img)

# pickle.dump(images, open("assets.dat", "wb"))

contact_frame = Frame(root, bg="#fff", width=356, height=555, highlightbackground="#808080", highlightthickness=2)
contact_frame.place(x=22, y=20)

Frame(contact_frame, height=40, width=2, bg="#7baad0").place(x=254, y=0)
Frame(contact_frame, height=2, width=356, bg="#808080").place(x=0, y=38)
empty_contact = Label(contact_frame, text="No contacts found", compound="top", image=images[0], fg="#505050", bg="#fff", font=("Verdana", 20))
Frame(contact_frame, height=2, width=356, bg="#808080").place(x=0, y=500)
Frame(contact_frame, height=50, width=2, bg="#7baad0").place(x=116, y=502)
Frame(contact_frame, height=50, width=2, bg="#7baad0").place(x=234, y=502)

detail_frame = Frame(root, bg="#fff", width=360, height=555, highlightbackground="#808080", highlightthickness=2)
detail_frame.place(x=398, y=20)

Label(detail_frame, image=images[1], bg="#fff").place(x=125, y=30)

title_frame = Frame(detail_frame, borderwidth=0, bg="#fff")

contact_title = Label(
    title_frame,
    font=("Arial", 15, "bold"),
    justify="center",
    width=26,
    padx=3,
    bg="#fff"
    )

contact_title.pack()

contact_info = Frame(
    detail_frame,
    borderwidth=2,
    relief="ridge",
    padx=4,
    bg="#fff",
    )

Label(
    contact_info,
    bg="#fff",
    text="Contact info",
    font=("Arial", 12, "bold")
    ).pack(side="top", anchor="w", padx=5, pady=5)

contact_number = Label(
    contact_info,
    image=images[7],
    compound="left",
    font=("Roboto", 12),
    anchor="w",
    width=290,
    padx=10,
    bg="#fff"
    )
contact_number.pack(pady=5)

contact_email = Label(
    contact_info,
    image=images[8],
    compound="left",
    font=("Roboto", 12),
    anchor="w",
    justify="left",
    width=290,
    padx=10,
    bg="#fff"
    )
contact_email.pack(pady=5)

contact_address = Label(
    contact_info,
    image=images[9],
    compound="left",
    font=("Roboto", 12),
    anchor="w",
    justify="left",
    width=290,
    padx=10,
    bg="#fff"
    )
contact_address.pack(pady=5)

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

def show_contact(event=None, getindex=-1):
    try:
        if getindex >= 0 :
            widget = event
            index = getindex
        else:
            widget = event.widget
            index = widget.curselection()[0]
        value = widget.get(index)
        getpass = True
        contact_title.config(text=value)
    except Exception:
        getpass = False

    if getpass:
        frame_line1.place_forget()
        frame_line2.place_forget()
        frame_line3.place_forget()
        frame_line4.place_forget()
        frame_line5.place_forget()
        title_frame.place(x=15, y=145)
        contact_info.place(x=15, y=200)
        # print(index)
        data = db_cursor.execute('SELECT * FROM list WHERE id = ?', (index,)).fetchone()
        id_, name, number, email, address = data
        # print(id_, name, number, email, address)

        if number:
            contact_number.config(text=number)
        else:
            contact_number.config(text="Add phone number")

        if email:
            contact_email.config(text=email)
        else:
            contact_email.config(text="Add email")
            
        if address:
            contact_address.config(text=address)
        else:
            contact_address.config(text="Add Address")

def hide_contact(event):
    frame_line1.place(x=95, y=160)
    frame_line2.place(x=35, y=240)
    frame_line3.place(x=35, y=320)
    frame_line4.place(x=35, y=400)
    frame_line5.place(x=35, y=480)
    contact_title.place_forget()
    contact_info.place_forget()

contact_list = Listbox(
    contact_frame,
    borderwidth=0,
    justify="center",
    activestyle="none",
    height=24, width=44,
    selectbackground="#b3ddff",
    selectforeground="#101010",
    highlightthickness=0,
    highlightcolor="#52b1ff",
    selectmode=EXTENDED,
    font=("Roboto", 11)
    )

contact_list.place(x=0, y=40)
contact_list.bind("<<ListboxSelect>>", show_contact)
# contact_list.bind("<Configure>", lambda e:print(e))
# contact_list.bind("<FocusOut>", hide_contact)

search_value = StringVar()
search_value.trace_add(callback=update_list, mode="write")

search_box = Entry(contact_frame, insertbackground="#505050", textvariable=search_value, fg="#505050", width=26, font=("Arial", 12), borderwidth=0)
search_placeholder = "Search contacts"
search_box.insert(0, search_placeholder)

# contact_title.config(textvariable=search_value)

def on_focus(event):
    if search_box.get() == search_placeholder:
        search_box.config(fg="#000")
        search_box.delete(0, END)

def on_leave(event):
    if search_box.get() == "":
        search_box.config(fg="#505050")
        search_box.insert(0, search_placeholder)

search_box.bind("<FocusIn>", on_focus)
search_box.bind("<FocusOut>", on_leave)
search_box.place(x=10, y=8)

search_btn = Button(contact_frame, fg="#fff", image=images[2], width=94, height=36,borderwidth=0, bg="#77C2FF", activebackground="#5cb3fb", activeforeground="#fff", pady=6, font=("Verdana", 12))
search_btn.place(x=256, y=0)
search_btn.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))
search_btn.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))

# update_list()

btn_text = ["Add", "Update", "Delete"]

add_btn = Button(contact_frame, command=add_dialog, width=90)
update_btn = Button(contact_frame, command=update_dialog, width=90)
delete_btn = Button(contact_frame, command=delete_contact, width=90)

add_btn.place(x=0, y=502)
update_btn.place(x=118,y=502)
delete_btn.place(x=236, y=502)

for index, widget in enumerate([add_btn, update_btn, delete_btn]):
    widget.config(
        text=btn_text[index],
        font=("Arial", 12),
        bg="#77C2FF",
        fg="#fff",
        activeforeground="#fff",
        activebackground="#77C2FF",
        borderwidth=0,
        image=images[index+3], compound="left",
        height=35,
        padx=12,
        pady=6
        )
    
    widget.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))
    widget.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))

root.mainloop()
