from sys import exit

try:
    from tkinter import (
        Y,
        Tk,
        END,
        Frame,
        Entry,
        Label,
        Button,
        Listbox,
        EXTENDED,
        Scrollbar
    )

    import sqlite3
    from PIL import ImageTk
    from pickle import load as pload
    from tkinter.messagebox import showinfo, askyesno

except ModuleNotFoundError as err:
    print(err)
    exit(1)

try:
    db_connection = sqlite3.connect("todolist.db") # Create database file if not exists and connecting to the database.
    db_cursor = db_connection.cursor()
    db_cursor.execute("CREATE TABLE if not exists todo(id int, task text)") # Create "tasks" named table if not exists.
    table_data = db_cursor.execute("select * from todo").fetchall()  # Retrieve all rows from the 'todo' table.
    table_data = [f"{row}\n" for index, row in enumerate(table_data) if index < len(table_data)]
    schema = db_cursor.execute("pragma table_info(todo)").fetchall()  # Retrieve the schema (column information) of the 'todo' table.
    schema = [f"{column}\n" for column in schema]
    # print("Database connection:", db_status, "\nSchema:\n", *schema, "Table data:\n", *table_data)
    db_status = True
except Exception as err:
    db_status = err

if not db_status == True:
    print("Something went wrong while initalizing database.")
    print(db_status)
    exit(1)

window_height = 680
window_width = 1080
font = "Helvetica"

class GUI(Tk):
    '''
    # GUI class inheriting from Tk, representing the main application window.
    '''
    def __init__(self):
        # Tk.__init__(self)
        super().__init__()  # Call the constructor of the superclass (Tk).
        self.title("TODO LIST")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the center coordinates for positioning the window.
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        
        # Set the geometry of the window to be centered on the screen.
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        self.config(bg="#fff")  # Set the main window background color to white.
        self.resizable(0,0)  # Disable window resizing.

        def confirm():
            """
            This function prompts the user with a confirmation dialog box asking if they want to exit.
            If the user confirms their intention to exit, the function destroys the associated GUI window.
            """
            ask = askyesno(title="Exit", message="Do You Want To Exit ?")
            if ask:
                self.destroy()  # Assuming 'self' refers to the GUI window object

        # Bind the confirm function to the window's protocol for deleting the window
        self.protocol("WM_DELETE_WINDOW", confirm)

    def frame(self, master, bg="#fff", padx=0, pady=0, border=0, width=0, height=0):
        return Frame(
    master=master, bg=bg,
    relief="solid",
    borderwidth=border,
    padx=padx, pady=pady,
    width=width, height=height
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
            cursor="hand2",
            borderwidth=0,
            activebackground="#77C2FF", bg="#77C2FF",
            font="Helvetica 11", command=command
            )

entry_placeholder = "Write something..."

def no_input():
    showinfo("Todo", "No input found, write something.")

def change_frame():
    '''
    This function change frame to empty style and task style,
    if todo_listbox have no such task it will change to empty style
    otherwise it will change frame to task style.
    '''
    task_count = todo_listbox.size()  # Get the number (length) of items in the todo list (todo_listbox) widget.
    # task_count = todo_listbox.index("end")

    if task_count == 0:
        todo_frame.config(pady=86, padx=31)
        for line in [line1, line2, line3, line4]:
            line.pack(pady=30)  # listing (adding) lines to the todo_frame

        todo_listbox.pack_forget()  # un-listing (removing) todo_listbox from todo_frame
        scrollbar.pack_forget()  # un-listing (removing) scrollbar from todo_frame
    else:
        for line in [line1, line2, line3, line4]:
            line.pack_forget()  # un-listing (removing) widgets from todo_frame
        
        todo_frame.config(padx=0, pady=0)
        todo_frame.place(x=460, y=110)
        todo_listbox.pack(side="left")  # Pack the todo list (todo_listbox) on the left side.
        scrollbar.pack(fill=Y, side="right")  # Pack the scrollbar on the right side and fill it along the Y-axis.
        scrollbar.config(command=todo_listbox.yview)  # Set command for scrolling items in the todo_listbox widget.
        todo_listbox.config(yscrollcommand=scrollbar.set)  # Set the count of items in the todo_listbox widget to the scrollbar.

def on_enter(e):
    task_entry.delete(0, END)  # Delete the entry_placeholder in the 'task_entry' widget.
    task_entry.config(fg="#000")  # set foreground color to 'task_entry' widget.
    add_button.config(command=add_task)  # Set the 'add_task' function as the command for the 'add_button' widget.
    update_button.config(command=update_task)  # Set the 'update_task' function as the command for the 'update_button' widget.

def on_leave(e):
    task_entry.delete(0, END)  # Delete the entire values of the 'task_entry' widget.
    task_entry.config(fg="#404040")  # set foreground color to 'task_entry' widget.
    task_entry.insert(0, entry_placeholder)  # Insert 'entry_placeholder' to the 'task_entry' widget.
    add_button.config(command=no_input)  # Set the 'no_input' function as the command for the 'add_button' widget.
    update_button.config(command=no_input)  # Set the 'no_input' function as the command for the 'update_button' widget.

def add_task(e=None):
    task = task_entry.get()

    if task:
        index = todo_listbox.index(END)  # Get the index of the last item in the todo list (todo_listbox) widget.
        todo_listbox.insert(END, task)  # Insert task to last (-1) of the todo list (todo_listbox) widget.
        todo_listbox.itemconfig(index, bg="#ebf6ff")  # Set background color to listbox items.
        db_cursor.execute('insert into todo (id, task) values (?, ?)', (index, task))  # inserting index and task to the todo table in database.
        change_frame()  # Call this function if any task added to the todo list (todo_listbox) widget.
        task_entry.delete(0, END)  # Delete the entire values from 'task_entry' after inserting them into 'todo_listbox'.
        showinfo("Todo", "Todo task has been added.")  # Show a dialog box after adding a task to the 'todo_listbox'. 
    else:
        no_input()  # Call this function if task (value of task_entry) not found.

def update_task():
    task = task_entry.get()

    if task:
        selections = todo_listbox.curselection()
        if not selections:
            showinfo("Todo", "Select one or more tasks to update.")
        for selection in selections:
            previous_task = todo_listbox.get(selection)
            todo_listbox.delete(selection)  # Delete 'todo_listbox' items by index.
            todo_listbox.insert(selection, task)  # Update 'todo_listbox' items by index.
            todo_listbox.itemconfig(selection, bg="#ebf6ff")  # Set background color to todo list (todo_listbox) widget items.
            db_cursor.execute('update todo set task = (?) where id = (?)', (task, selection))  # Update tasks in database by index.
        task_entry.delete(0, END)  # Delete the entire values from 'task_entry' after updating them into 'todo_listbox'.
    else:
        no_input()  # Call this function if task (value of task_entry) not found.

def remove_task():
    selections = todo_listbox.curselection()  # Get the indexes of the selected items in the todo list (todo_listbox) widget.
    for selection in reversed(selections):
        task = todo_listbox.get(selection)  # Retrieve the name of the item selected in the todo list (todo_listbox) widget.
        todo_listbox.delete(selection)  # Delete 'todo_listbox' items by index.
        db_cursor.execute('delete from todo where task = (?) and id = (?)', (task,selection))
    tasks = todo_listbox.get(0, END)  # Get all 'todo_task' items from starting (0) to end (-1)
    db_cursor.execute('delete from todo')   # Delete all contents from the todo table in database.
    for index, task in enumerate(tasks):
        db_cursor.execute('insert into todo (id, task) values (?, ?)', (index, task))  # inserting index and task to the todo table in database.
    if not selections:
        showinfo("Todo", "Select one or more tasks to delete.")  # Show a dialog box if 'todo_listbox' items not selected.
    else:
        change_frame()  # Call this function if any task removed from todo list (todo_listbox) widget.

def delete_all():
    tasks = todo_listbox.get(0, END)  # Get all 'todo_task' items from starting (0) to end (-1)
    if tasks:
        db_cursor.execute('delete from todo')  # Delete all contents from the todo table in database.
        todo_listbox.delete(0, END)  # Remove all 'todo_task' items from starting (0) to end (-1)
    else:
        showinfo("Todo", "Todo list is empty.")  # Show a dialog box if tasks (todo_lisbox items) not found.

if __name__ == "__main__":
    window = GUI()

    image_coordinates = [
        (380, 6),
        (-15, -15),
        (window_width-220, -10),
        (-145, 485),
        (window_width-216, 505),
        (10, 145)
        ]

    images = []
    image_data = pload(open("assets.dat", "rb"))  # Load data from 'assets.dat' file as an object using pickle.
    button_data = image_data[-1]  # Retrieve the last element from the 'image_data'
    image_data.pop()  # Remove last element of the list

    for index, image in enumerate(image_data):
        images.append(ImageTk.PhotoImage(image))  # Convert the image object to Tkinter compatible format and store it in the 'images' list.
        x, y = image_coordinates[index]  # Unpack the tuple at the specified index and assign its values to 'x' and 'y'.
        Label(master=window, image=images[-1], bg="#fff").place(x=x, y=y)

    todo_frame = window.frame(window, border=1)
    todo_frame.place(x=460, y=110)

    line1 = window.frame(todo_frame, height=2, width=400, bg="#505050")
    line2 = window.frame(todo_frame, height=2, width=400, bg="#505050")
    line3 = window.frame(todo_frame, height=2, width=400, bg="#505050")
    line4 = window.frame(todo_frame, height=2, width=400, bg="#505050")
    
    entry_frame = window.frame(window, padx=10, pady=10, border=1)
    entry_frame.place(x=460, y=555)

    option_frame = window.frame(window, padx=10, pady=10)
    option_frame.place(x=530, y=605)

    scrollbar = Scrollbar(todo_frame, borderwidth=0, border=0)

    todo_listbox = Listbox(
        master=todo_frame,
        width=63, height=22, activestyle="none",
        fg="#202020", bg="#fff", selectborderwidth=1,
        borderwidth=0, border=0, justify="center",
        selectmode=EXTENDED, selectbackground="#77C2FF",
        selectforeground="#202020", font="Helvetica 10"
        )

    tasks = [row[0] for row in db_cursor.execute("select task from todo")]  # storing tasks from database

    todo_listbox.insert(0, *tasks)  # inserting tasks from database to listbox

    task_count = todo_listbox.size()  # get length listbox items

    for index in range(task_count):
        todo_listbox.itemconfig(index, bg="#ebf6ff")  # set background color to listbox items

    change_frame()  # call this function after fetching tasks from database

    image = ImageTk.PhotoImage(button_data)

    window.buttonShape(option_frame, image)

    task_entry = Entry(entry_frame, width=55, justify="center", borderwidth=0, font="Helvetica 11", fg="#404040")
    task_entry.pack()

    task_entry.insert(0, entry_placeholder)  # Set the initial placeholder text in the 'task_entry' widget.
    task_entry.bind("<Return>", add_task)  # Bind 'Return' event to trigger 'add_task' function when 'Enter' key is pressed.
    task_entry.bind("<FocusIn>", on_enter)  # Bind 'FocusIn' event to trigger 'on_enter' function when 'task_entry' widget receives focus.
    task_entry.bind("<FocusOut>", on_leave)  # Bind 'FocusOut' event to trigger 'on_leave' function when focus leaves the 'task_entry' widget.

    add_button = window.button(option_frame, text="Add", command=no_input)
    add_button.place(x=32, y=7)

    update_button = window.button(option_frame, text="Update", command=no_input)
    update_button.place(x=122, y=7)

    remove_button = window.button(option_frame, text="Remove", command=remove_task)
    remove_button.place(x=218, y=7)

    window.mainloop()  # Run the tkinter event loop.

db_connection.commit()  # Commit changes to the database
