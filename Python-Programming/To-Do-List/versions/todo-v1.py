import sqlite3 as db
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

root = Tk()
root.title("TODO LIST")
root.config(bg="#fff")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_height = 680
window_width = 1080

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
root.resizable(0,0)

entry_placeholder = "Write something..."

def on_leave(e):
    entry.delete(0, END)
    entry.insert(0, entry_placeholder)

def add_task():
    if entry.get():
        todo_listbox.insert(END, entry.get())
        messagebox.showinfo("Todo", "Todo task has been added.")

def update_task():
    if entry.get():
        selections = todo_listbox.curselection()
        for selection in selections:
            todo_listbox.delete(selection)
            todo_listbox.insert(selection, entry.get())
        entry.delete(0, END)

def delete_task():
    selections = todo_listbox.curselection()
    for selection in reversed(selections):
        todo_listbox.delete(selection)

def delete_all():
    todo_listbox.delete(0, END)

image_path = "images/"
image_list = [
    image_path + "wave-left.png",
    image_path + "wave-right.png",
    image_path + "wave-bottom-left.png",
    image_path + "wave-bottom-right.png",
    image_path + "todo-poster.png"
    ]

image_size = [
    (250, 150),
    (250, 150),
    (320, 320),
    (356, 356),
    (386, 326)
    ]

image_coordinates = [
    (-15, -15),
    (window_width-220, -10),
    (-145, 485),
    (window_width-216, 505),
    (10, 145)
    ]

images = []

for index, image in enumerate(image_list):
    image = Image.open(image)
    resize = image.resize(image_size[index])
    images.append(ImageTk.PhotoImage(resize))
    x, y = image_coordinates[index]
    Label(image=images[-1], bg="#fff").place(x=x, y=y)

todo_frame = Frame(
    master=root, bg="#fff",
    relief="solid",
    borderwidth=1,
    padx=10, pady=10
    )
todo_frame.place(x=460, y=110)

entry_frame = Frame(
    master=root, bg="#fff",
    relief="solid",
    borderwidth=1,
    padx=9, pady=10
    )
entry_frame.place(x=460, y=560)

option_frame = Frame(
    master=root, bg="#fff",
    # relief="sunken",
    # borderwidth=1,
    padx=10, pady=10
    )
option_frame.place(x=525, y=610)

scrollbar = Scrollbar(todo_frame, borderwidth=0, border=0)
scrollbar.pack(fill=Y, side="right")

todo_listbox = Listbox(master=todo_frame, width=60, height=19, borderwidth=0, border=0, selectborderwidth=2, selectmode=EXTENDED, selectbackground="#77C2FF", selectforeground="#202020", font="Helvetica 10")
todo_listbox.pack()

todo_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=todo_listbox.yview)

for item in range(21):
    todo_listbox.insert(END, item)

entry = Entry(entry_frame, width=55, justify="center", borderwidth=0, font="Helvetica 11")
entry.pack()

entry.insert(0, entry_placeholder)
entry.bind("<FocusIn>", lambda e:entry.delete(0, END))
entry.bind("<FocusOut>", on_leave)

photo = Image.open("images/round button.png")
resize = photo.resize((80, 40))
image = ImageTk.PhotoImage(resize)

Label(option_frame, image=image, borderwidth=0, bg="white").pack(side="left", padx=10)
Label(option_frame, image=image, borderwidth=0, bg="white").pack(side="left", padx=10)
Label(option_frame, image=image, borderwidth=0, bg="white").pack(side="left", padx=10)

add_button = Button(option_frame, padx=10, pady=6, text="Add", borderwidth=0, activebackground="#77C2FF", bg="#77C2FF", font="Helvetica 11", command=add_task)
add_button.place(x=24, y=2)

update_button = Button(option_frame, text="Update", borderwidth=0, activebackground="#77C2FF", bg="#77C2FF", font="Helvetica 11", command=update_task)
update_button.place(x=122, y=7)

delete_button = Button(option_frame, text="Remove", borderwidth=0, activebackground="#77C2FF", bg="#77C2FF", font="Helvetica 11", command=delete_task)
delete_button.place(x=218, y=7)

root.mainloop()
