import pickle
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

window_height = 680
window_width = 1080

class GUI(Tk):
    def __init__(self):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.title("TODO LIST")
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.config(bg="#fff")
        self.resizable(0,0)

    def frame(self, master, padx=0, pady=0, border=0):
        return Frame(
    master=master, bg="#fff",
    relief="solid",
    borderwidth=border,
    padx=padx, pady=pady
    )

    @staticmethod
    def buttonShape(master, image):
        count = 3
        for _ in range(count):
            Label(master=master, image=image, borderwidth=0, bg="white").pack(side="left", padx=10)

    def button(self, master, text, command=None):
        return Button(
            master=master,
            text=text,
            borderwidth=0,
            activebackground="#77C2FF", bg="#77C2FF",
            font="Helvetica 11", command=command
            )

entry_placeholder = "Write something..."

def no_input():
    messagebox.showinfo("Todo", "No input found, write something.")

def on_enter(e):
    entry.delete(0, END)
    entry.config(fg="#000")
    add_button.config(command=add_task)
    update_button.config(command=update_task)

def on_leave(e):
    entry.delete(0, END)
    entry.config(fg="#404040")
    entry.insert(0, entry_placeholder)
    add_button.config(command=no_input)
    update_button.config(command=no_input)

def add_task():
    if entry.get():
        todo_listbox.insert(END, entry.get())
        messagebox.showinfo("Todo", "Todo task has been added.")
    else:
        no_input()

def update_task():
    if entry.get():
        selections = todo_listbox.curselection()
        if not selections:
            messagebox.showinfo("Todo", "Select one or more tasks to update.")
        for selection in selections:
            todo_listbox.delete(selection)
            todo_listbox.insert(selection, entry.get())
        entry.delete(0, END)
    else:
        no_input()

def delete_task():
    selections = todo_listbox.curselection()
    for selection in reversed(selections):
        todo_listbox.delete(selection)
    if not selections:
        messagebox.showinfo("Todo", "Select one or more tasks to delete.")

def delete_all():
    todo_listbox.delete(0, END)

if __name__ == "__main__":
    window = GUI()

    image_path = "images/"
    image_list = [
        "todo-logo.png",
        "wave-left.png",
        "wave-right.png",
        "wave-bottom-left.png",
        "wave-bottom-right.png",
        "todo-poster.png"
        ]
    image_list = [image_path + image for image in image_list]

    image_size = [
        (350, 55),
        (250, 150),
        (250, 150),
        (320, 320),
        (356, 356),
        (386, 326)
        ]

    image_coordinates = [
        (340, 10),
        (-15, -15),
        (window_width-220, -10),
        (-145, 485),
        (window_width-216, 505),
        (10, 145)
        ]

    images = []
    image_data = []

    for index, image in enumerate(image_list):
        image = Image.open(image)
        resize = image.resize(image_size[index])
        image_data.append(resize)
        images.append(ImageTk.PhotoImage(resize))
        x, y = image_coordinates[index]
        Label(master=window, image=images[-1], bg="#fff").place(x=x, y=y)

    photo = Image.open("images/round button.png")
    resize = photo.resize((80, 40))
    image = ImageTk.PhotoImage(resize)

    image_data.append(resize)
    pickle.dump(image_data, open("assets.dat", "wb"))

    todo_frame = window.frame(window, padx=10, pady=10, border=1)
    todo_frame.place(x=460, y=110)
    
    entry_frame = window.frame(window, padx=9, pady=10, border=1)
    entry_frame.place(x=460, y=560)

    option_frame = window.frame(window, padx=10, pady=10)
    option_frame.place(x=525, y=610)

    scrollbar = Scrollbar(todo_frame, borderwidth=0, border=0)
    scrollbar.pack(fill=Y, side="right")

    todo_listbox = Listbox(master=todo_frame, width=60, height=19, borderwidth=0, border=0, selectborderwidth=2, selectmode=EXTENDED, selectbackground="#77C2FF", selectforeground="#202020", font="Helvetica 10")
    todo_listbox.pack()

    todo_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=todo_listbox.yview)

    for item in range(21):
        todo_listbox.insert(END, item)

    window.buttonShape(option_frame, image)

    entry = Entry(entry_frame, width=55, justify="center", borderwidth=0, font="Helvetica 11", fg="#404040")
    entry.pack()

    entry.insert(0, entry_placeholder)
    # entry.bind("<Return>", )
    entry.bind("<FocusIn>", on_enter)
    entry.bind("<FocusOut>", on_leave)

    add_button = window.button(option_frame, text="Add", command=no_input)
    add_button.place(x=32, y=7)

    update_button = window.button(option_frame, text="Update", command=no_input)
    update_button.place(x=122, y=7)

    delete_button = window.button(option_frame, text="Remove", command=delete_task)
    delete_button.place(x=218, y=7)

    window.mainloop()

