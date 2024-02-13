from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps 
from tkinter import messagebox

# messagebox.showinfo("Hello", "Hello")

root = Tk()
root.title("Contact Book")
root.geometry("600x700+450+100")

def add_dialog():
    add_window = Toplevel(root)
    add_window.config(bg="#fff")
    add_window.geometry("400x300+550+400")
    add_window.title("Add Contact")
    # add_window.focus_force()
    add_window.resizable(0, 0)
    # add_window.attributes('-toolwindow', True)
    add_window.grab_set()

    main_frame = Frame(add_window, bg="#fff")
    main_frame.pack(pady=20)

    # Frame(main_frame, width=162, height=20, bg="#77C2FF").place(x=62, y=25)
    # Frame(main_frame, width=162, height=20, bg="#77C2FF").place(x=62, y=53)
    # Frame(main_frame, width=162, height=20, bg="#77C2FF").place(x=62, y=80)
    # Frame(main_frame, width=162, height=20, bg="#77C2FF").place(x=62, y=108)

    # Label(main_frame, width=7, bg="#fff", text="Name", font=("Verdana", 10), anchor="w").grid(row=0, column=0)
    # Label(main_frame, width=7, bg="#fff", text="Number", font=("Verdana", 10), anchor="w").grid(row=1, column=0)
    # Label(main_frame, width=7, bg="#fff", text="Email", font=("Verdana", 10), anchor="w").grid(row=2, column=0)
    # Label(main_frame, width=7, bg="#fff", text="Address", font=("Verdana", 10), anchor="w").grid(row=3, column=0)

    entry_frm1 = Frame(main_frame, width=250, height=35, bg="#fff", highlightthickness=1, highlightbackground="#77C2FF", highlightcolor="#77C2FF")
    entry_frm2 = Frame(main_frame, width=250, height=35, bg="#fff", highlightthickness=1, highlightbackground="#77C2FF", highlightcolor="#77C2FF")
    entry_frm3 = Frame(main_frame, width=250, height=35, bg="#fff", highlightthickness=1, highlightbackground="#77C2FF", highlightcolor="#77C2FF")
    entry_frm4 = Frame(main_frame, width=250, height=35, bg="#fff", highlightthickness=1, highlightbackground="#77C2FF", highlightcolor="#77C2FF")
    entry_frm1.pack(pady=5)
    entry_frm2.pack(pady=5)
    entry_frm3.pack(pady=5)
    entry_frm4.pack(pady=5)


    def on_focus(e, widget, word):
        global label_text
        if word == "Name":
            y = -5
        elif word == "Number":
            y = 40
        elif word == "Email":
            y = 85
        elif word == "Address":
            y = 130

        if widget.get() == word:
            label_text = Label(main_frame, bg="#fff", borderwidth=0)
            label_text.config(text=word)
            label_text.place(x=5, y=y)
            widget.delete(0, END)
        widget.config(fg="#000")

    def on_leave(e, widget, word):
        if not widget.get():
            label_text.place_forget()
            widget.insert(0, word)
            widget.config(fg="#303030")

    name_entry = Entry(entry_frm1, fg="#303030", width=29, font=("Arial", 11), borderwidth=0)
    number_entry = Entry(entry_frm2, fg="#303030", width=29, font=("Arial", 11), borderwidth=0)
    email_entry = Entry(entry_frm3, fg="#303030", width=29, font=("Arial", 11), borderwidth=0)
    address_entry = Entry(entry_frm4, fg="#303030", width=29, font=("Arial", 11), borderwidth=0)

    name_entry.place(x=7, y=6)
    number_entry.place(x=7, y=6)
    email_entry.place(x=7, y=6)
    address_entry.place(x=7, y=6)

    name_entry.bind("<FocusIn>", lambda e : on_focus(e, name_entry, "Name"))
    name_entry.bind("<FocusOut>", lambda e : on_leave(e, name_entry, "Name"))

    number_entry.bind("<FocusIn>", lambda e : on_focus(e, number_entry, "Number"))
    number_entry.bind("<FocusOut>", lambda e : on_leave(e, number_entry, "Number"))

    email_entry.bind("<FocusIn>", lambda e : on_focus(e, email_entry, "Email"))
    email_entry.bind("<FocusOut>", lambda e : on_leave(e, email_entry, "Email"))

    address_entry.bind("<FocusIn>", lambda e : on_focus(e, address_entry, "Address"))
    address_entry.bind("<FocusOut>", lambda e : on_leave(e, address_entry, "Address"))

    name_entry.insert(0, "Name")
    number_entry.insert(0, "Number")
    email_entry.insert(0, "Email")
    address_entry.insert(0, "Address")

    name_entry.focus_force()

    bottom_frame = Frame(
        add_window,
        # bg="#e2e2e2"
        bg="#fff"
        )
    # bottom_frame.pack(fill=X, side="bottom")
    bottom_frame.pack(fill=X)

    save_btn = Button(bottom_frame, image=images[-1], bg="#77C2FF", highlightcolor="#000", highlightbackground="#77C2FF", highlightthickness=2, activebackground="#77C2FF", pady=5, width=200, height=30, borderwidth=0, font=("Verdana", 10))
    save_btn.pack(padx=20, pady=5)

    # save_btn = Button(bottom_frame, text="Save", height=2, width=8, borderwidth=2, relief="groove", font=("Verdana", 10))
    # cancel_btn = Button(bottom_frame, text="Cancel", height=2, width=8, borderwidth=2, relief="groove", font=("Verdana", 10))
    # save_btn.pack(side="left", padx=20, pady=5)
    # cancel_btn.pack(side="right", padx=20, pady=5)

    # cancel_btn.bind("<Button-1>", lambda e: add_window.destroy())

def update_dialog():
    pass

def delete_contact():
    pass

bottom_frame = Frame(root)
bottom_frame.pack(fill=X, side="bottom")

image_path = ["images/plus.png", "images/edit.png", "images/trash.png", "images/save.png"]
images = []

for index, image in enumerate(image_path):
    if index >= 2:
        x, y = 18, 20
    else:
        x, y = 20, 20
    image = Image.open(image).resize((x, y))
        # Separate the image into channels (R, G, B, A)
    r, g, b, a = image.split()

    # Invert the RGB channels
    r = Image.eval(r, lambda x: 255)
    g = Image.eval(g, lambda x: 255)
    b = Image.eval(b, lambda x: 255)

    # Combine the inverted RGB channels with the original alpha channel
    inverted_img = Image.merge('RGBA', (r, g, b, a))
    images.append(ImageTk.PhotoImage(inverted_img))

bottom_center_frame = Frame(bottom_frame)
bottom_center_frame.pack(pady=20)

add_btn = Button(bottom_center_frame, image=images[0], borderwidth=2, width=40, height=40, relief="ridge", bg="#77C2FF", activebackground="#77C2FF", command=add_dialog)
update_btn = Button(bottom_center_frame, image=images[1], borderwidth=2, width=40, height=40, relief="ridge", bg="#77C2FF", activebackground="#77C2FF", command=update_dialog)
delete_btn = Button(bottom_center_frame, image=images[2], borderwidth=2, width=40, height=40, relief="ridge", bg="#77C2FF", activebackground="#77C2FF", command=delete_contact)

add_btn.pack(side="left", padx=10)
update_btn.pack(side="left", padx=10)
delete_btn.pack(side="left", padx=10)

root.mainloop()
