from sys import exit

try:
    from tkinter import (
        X,
        Tk,
        END,
        Frame,
        Entry,
        Label,
        Button,
        Listbox,
        EXTENDED,
        Toplevel,
        StringVar,
        BooleanVar,
    )

    import sqlite3
    from PIL import ImageTk
    from re import match as rmatch
    from pickle import load as pload
    from tkinter.messagebox import showinfo, showwarning, askquestion
except ModuleNotFoundError as err:
    print(err)
    exit(1)

try:
    # Create database file if not exists and connecting to the database.
    db_connection = sqlite3.connect("contacts.db")
    db_cursor = db_connection.cursor()
    
    # Create the 'list' table if it does not already exist, with specified columns.
    db_cursor.execute("CREATE TABLE if not exists list(id int, name text, number int, email text, address text)")

    table_data = db_cursor.execute("select * from list").fetchall()  # Retrieve all rows from the 'list' table.
    db_status = True
except Exception as err:
    db_status = err

if not db_status == True:
    print("Something went wrong while initalizing database.")
    print(db_status)
    exit(1)

def update_global_data():
    """
    Update the global_data list with names from the list table in the database.
    """
    global global_data
    # Retrieve the names from the list table in the database and store them in global_data
    global_data = [row[0] for row in db_cursor.execute('SELECT name FROM list')]

# Update global_data with names from database
update_global_data()

root = Tk()  # Create a tkinter root window.
root.title("Contact Book")

window_width = 780
window_height = 600

# Get the screen width and height.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center coordinates for positioning the window.
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

# Set the geometry of the window to be centered on the screen.
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

root.config(bg="#fff")  # Set the main window background color to white.
root.resizable(0, 0)  # Disable window resizing.

images = []
image_data = pload(open("assets.dat", "rb"))  # Load data from 'assets.dat' file as an object using pickle.

for image in image_data:
    images.append(ImageTk.PhotoImage(image))  # Convert the image object to Tkinter compatible format and store it in the 'images' list.

def add_dialog(window_title="Add contact", index_id=-1, title="", number="", email="", address=""):
    """
    Function to create and display a dialog window for adding or updating a contact.

    Args:
        window_title: The title of the dialog window (default is "Add contact").
        index_id: The ID of the contact to edit (default is -1).
        title: The name of the contact (default is an empty string).
        number: The phone number of the contact (default is an empty string).
        email: The email address of the contact (default is an empty string).
        address: The address of the contact (default is an empty string).
    """
    add_window = Toplevel(root)  # Create a new Toplevel window

    top_window_width = 320
    top_window_height = 400

    # Sets custom coordinates of the 'add_window' of root window.
    x_add_window = int(x_cordinate + window_width * 0.0520)
    y_add_window = int(y_cordinate + window_height * 0.3)

    # Set the geometry of the add_window
    add_window.geometry(f"{top_window_width}x{top_window_height}+{x_add_window}+{y_add_window}")
    
    add_window.title(window_title)
    add_window.config(bg="#fff")
    # add_window.focus_force()
    add_window.resizable(0, 0)
    # add_window.attributes('-toolwindow', True)
    add_window.grab_set()

    Label(add_window, image=images[1], bg="#fff").pack(pady=10)

    main_frame = Frame(add_window, bg="#fff")
    main_frame.pack()

    entry_frame_options = dict(
        master=main_frame,
        width=250,height=35,
        highlightthickness=1,
        highlightcolor="#52b1ff",
        highlightbackground="#303030",
        background="#fff"
        )

    entry_frm1 = Frame(**entry_frame_options)
    entry_frm2 = Frame(**entry_frame_options)
    entry_frm3 = Frame(**entry_frame_options)
    entry_frm4 = Frame(**entry_frame_options)

    entry_frames = [entry_frm1, entry_frm2, entry_frm3, entry_frm4]
    
    for entry_frame in entry_frames:
        entry_frame.pack(pady=10)

    # List of entry exceptions.
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
        """
        Function to handle the focus event for entry widgets.

        Args:
            event: The event that triggers the function.
            word: The placeholder text.
        """
        # Set pword to the placeholder text
        global pword
        pword = word

        # Get the widget that triggered the event
        widget = event.widget

        # If the value of number_entry is equal to the placeholder, change its color and clear the text
        if number_entry.get() == entry_exceptions[3]:
            number_entry.delete(0, END)  # Clear all the text from number_entry.
            number_entry.config(fg="#808080")  # Set foreground color to dark grey.
            number_entry.insert(0, number_placeholder)  # Insert placeholder text to number_entry.

        # If the widget's text is equal to the placeholder or one of the entry_exceptions, clear the text
        if widget.get() == word or widget.get() in entry_exceptions:
            widget.delete(0, END)  # Clear all text from widget.
        widget.config(fg="#1f1f1f")  # Set widget foreground color to dark.

    def on_leave(event):
        """
        Function to handle the leave event for entry widgets.

        Args:
            event: The event that triggers the function.
        """
        word = pword

        # Get the widget that triggered the event
        widget = event.widget

        # If the widget's text is empty, insert the placeholder text and change its color
        if not widget.get():  # Check if it's not empty (have value).
            widget.insert(0, word)  # Clear all text from widget.
            widget.config(fg="#808080")  # Set foreground color to dark grey.

    # Set variables to store boolean values.
    titlelen = BooleanVar()
    numberlen = BooleanVar()
    isnumber = BooleanVar()
    emaillen = BooleanVar()
    isemail = BooleanVar()
    addresslen = BooleanVar()

    def save_data():
        """
        Function to save the entered contact details to the database and update the contact listbox.
        """
        # Split the name, email, and address entries based on the split_character function
        name = split_character(name_entry.get())
        number = number_entry.get()
        email = split_character(email_entry.get())
        address = split_character(address_entry.get())

        title = ""
        _number = ""
        _email = ""
        _address = ""

        # Create a dictionary containing the variables name, number, email, and address
        variables = {
            "name":name,
            "number":number,
            "email":email,
            "address":address
        }

        # Create a list of empty variables if placeholder in value or values are empty.
        empty_variables = [
            key for key, value in variables.items()
            if value in [name_placeholder, number_placeholder, email_placeholder, address_placeholder] or not value
            ]

        # print(empty_variables)
        field = False

        # Check if both "name" and "number" are in the list of empty variables
        if "name" in empty_variables and "number" in empty_variables:
            showwarning("Add contact", entry_exceptions[0], parent=add_window)
            add_window.focus_force()  # Focus on the add_window

        # Check if neither "name" nor "number" are in the list of empty variables
        if not "name" in empty_variables and not "number" in empty_variables:
            title = name  # Set title to name
            _number = number  # Set _number to number
            if isnumber.get():
                field = True
            else:
                field = False

        # Check if "name" is not in the list of empty variables
        elif not "name" in empty_variables:
            title = name
            field = True

        # Check if "number" is not in the list of empty variables
        elif not "number" in empty_variables:
            title = number  # Set title to number
            _number = number  # Set _number to number
            if isnumber.get():
                field = True
            else:
                field = False

        # Check if "email" is not in the list of empty variables
        if not "email" in empty_variables:
            _email = email  # Set _email to email.
            validate_email(widget=email_entry)  # Validate the email entry widget
            if isemail.get():
                field = True
            else:
                field = False

        # If "address" is not in the empty_variables list, set _address to address
        if not "address" in empty_variables:
            _address = address

        # print(f"titlelen: {titlelen.get()}\nnumberlen: {numberlen.get()}\nisnumber: {isnumber.get()}\nemaillen: {emaillen.get()}\nisemail: {isemail.get()}\naddresslen: {addresslen.get()}")
        # print(f"title: {title}\nnumber: {_number}\nemail: {_email}\naddress: {_address}")

        if field:  # Check if filed is True.
            index = contact_list.index(END)  # Get the index of the last item in the contact list
            # print(index)
            if index_id >= 0:  # Checks if index_id is greater than or equal to 0.
                index = index_id # Update index to index_id

                # Delete the contact at index_id from the contact list
                contact_list.delete(index_id)

                # Insert the contact with the updated title at index_id in the contact list
                contact_list.insert(index_id, title)
                """
                Update the contact details in the list table in the database
                using the provided title, number, email, and address for the specified index
                """
                db_cursor.execute("update list set (name, number, email, address) = (?, ?, ?, ?) where id = (?)", (title, _number, _email, _address, index_id))

                # Update the contact title label with the provided title
                contact_title.config(text=title)

                # Update the contact number label with the provided number if available; otherwise, set it to "Add phone number"
                if _number:
                    contact_number.config(text=_number)
                else:
                    contact_number.config(text="Add phone number")

                # Update the contact email label with the provided email if available; otherwise, set it to "Add email"
                if _email:
                    contact_email.config(text=_email)
                else:
                    contact_email.config(text="Add email")

                # Update the contact address label with the provided address if available; otherwise, set it to "Add Address"
                if _address:
                    contact_address.config(text=_address)
                else:
                    contact_address.config(text="Add Address")
            else:
                # Insert the title into the end of the contact list
                contact_list.insert(END, title)
                # inserting contact details to the list table in database.
                db_cursor.execute('insert into list (id, name, number, email, address) values (?, ?, ?, ?, ?)', (index, title, _number, _email, _address))
            # contact_list.select_set(index)
                
            # Call the show_contact function with the event as contact_list and getindex as index
            show_contact(event=contact_list, getindex=index)
            db_connection.commit()  # Commit the changes to the database
            add_window.destroy()  # Destroy the add_window
            update_global_data()  # Update global_data with names from database
            change_frame()  # Call the change_frame function.

    label_options = dict(master=main_frame, bg="#fff", borderwidth=0, font=("Arial", 8, "bold"))

    name_lbl = Label(text="Name", **label_options)
    number_lbl = Label(text="Number", **label_options)
    email_lbl = Label(text="Email", **label_options)
    address_lbl = Label(text="Address", **label_options)

    name_lbl.place(x=5, y=2)
    number_lbl.place(x=5, y=57)
    email_lbl.place(x=5, y=112)
    address_lbl.place(x=5, y=167)

    def config_entry( widget, value=None, count=0):
        """
        Function to configure an entry widget.

        Args:
            widget: The entry widget to configure.
            value: The value to set for the widget (default is None).
            count: The number of times the function has been called (default is 0).
        """
        widget.config(fg="#1f1f1f")  # Restore widget foreground color for text.
        widget.delete(0, END)  # Clear all text from the widget.

        if value:
            if value in placeholders:  # Check if the value is one of the placeholders
                widget.config(fg="#808080")  # Restore widget foreground color for placeholder.
                widget.insert(0, value)  # Insert (add) values to the widget.
            else:
                widget.insert(0, value[0:count])  # Insert (add) values up to 'count'.

    def validate_name(*args):
        """
        Function to validate a name.

        Args:
            *args: Additional arguments.
        """
        name = name_value.get()  # Get values of 'name_value' and store it in 'name' variable.

        if not name == "Full Name":
            if len(name) > 25:
                titlelen.set(False)  # Set titilelen to False
                tmpValue = name  # Store name in tmpValue variable.
                name_entry.config(fg="#ff6969")  # Change name_entry foreground color.
                name_value.set(entry_exceptions[2])  # Set value as entry_exceptions for 'name_value'.

                # Schedule config_entry function with arguments to be called after 1 second
                name_entry.after(1000, config_entry, name_entry, tmpValue, 25)
                add_window.focus_force()  # Set focus to add_window immediately.
            else:
                if len(name) > 0:   # If the length of the name is greater than 0, set titlelen to True
                    titlelen.set(True)
        else:
            titlelen.set(False)  # Set titlelen to False

    def validate_number(*args):
        """
        Function to validate a phone number.

        Args:
            *args: Additional arguments.
        """
        number = number_value.get()

        if not number == "Number":
            if len(number) > 20:
                numberlen.set(False)  # Set numberlen to False
                if not number == entry_exceptions[3]:
                    tmpValue = number  # Store number in tmpValue variable.
                    number_entry.config(fg="#ff6969")  # Change number_entry foreground color.
                    number_value.set(entry_exceptions[3])  # Set value as entry_exceptions for 'number_value'.
                    
                    # Schedule config_entry function with arguments to be called after 1 second
                    number_entry.after(1000, config_entry, number_entry, tmpValue, 20)
                    add_window.focus_force()  # Set focus to add_window immediately.
            else:
                if len(number) > 0:  # If the length of the number is greater than 0, set numberlen to True
                    numberlen.set(True)

                if number.isdigit():
                    isnumber.set(True)  # Set isnumber to True
                    number_entry.config(fg="#1f1f1f")  # Change number_entry foreground color.
                    number_value.set(number)  # Set the value of number_value to the given variable.
                else:
                    isnumber.set(False)  # Set numberlen to False
                    # number_value.set("")
                    if number.isalpha():
                        number_entry.config(fg="#ff6969")  # Change number_entry foreground color.
                        number_value.set(entry_exceptions[1])  # Set value as entry_exceptions for 'number_value'.
                        
                        # Schedule config_entry function with arguments to be called after 1 second
                        number_entry.after(1000, config_entry, number_entry, "Number")
                        add_window.focus_force()  # Set focus to add_window immediately.
        else:
            numberlen.set(False)  # Set numberlen to False

    def validate_email(widget=None, *args):
        """
        Function to validate an email address.

        Args:
            widget: The widget to display error message (default is None).
            *args: Additional arguments.
        """
        email = email_value.get()

        try:
            widget.get()
            # Regular expression pattern for validating email addresses
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
            # Use re.match to search the pattern in the given email
            if not rmatch(pattern, email):
                if not email == "Email" and email:
                    isemail.set(False)  # Set isemail to False
                    tmpValue = email  # Store email in tmpValue variable.
                    email_entry.config(fg="#ff6969")  # Change email_entry foreground color.
                    email_value.set(entry_exceptions[5])  # Set value as entry_exceptions for 'email_value'.

                    # Schedule config_entry function with arguments to be called after 1 second
                    address_entry.after(1000, config_entry, email_entry, tmpValue, len(tmpValue))
                    add_window.focus_force()  # Set focus to add_window immediately.
                else:
                    emaillen.set(False)  # Set emaillen to False
            else:
                isemail.set(True)  # Set isemail to True

        except Exception:

            if not email == "Email":
                if len(email) > 63:
                    emaillen.set(False)  # Set emaillen to False
                    tmpValue = email  # Store email in tmpValue variable.
                    email_entry.config(fg="#ff6969")  # Change email_entry foreground color.
                    email_value.set(entry_exceptions[4])  # Set value as entry_exceptions for 'email_value'.

                    # Schedule config_entry function with arguments to be called after 1 second
                    address_entry.after(1000, config_entry, email_entry, tmpValue, 63)
                    add_window.focus_force()  # Set focus to add_window immediately.
                else:
                    if len(email) > 0:  # If the length of the email is greater than 0, set emaillen to True
                        emaillen.set(True)
            else:
                emaillen.set(False)  # Set emaillen to False

    def validate_address(*args):
        """
        Function to validate an address.

        Args:
            *args: Additional arguments.
        """
        address = address_value.get()

        if not address == "Address":
            if len(address) > 100:
                addresslen.set(False)  # Set addresslen to False
                tmpValue = address  # Store address in tmpValue variable.
                address_entry.config(fg="#ff6969")  # Change address_entry foreground color.
                address_value.set(entry_exceptions[6])  # Set value as entry_exceptions for 'address_value'.
                address_entry.after(1000, config_entry, address_entry, tmpValue, 100)
                add_window.focus_force()  # Set focus to add_window immediately.
            else:
                if len(address) > 0:  # If the length of the address is greater than 0, set addresslen to True
                    addresslen.set(True)
        else:
            addresslen.set(False)  # Set addresslen to False

    # Set variables to store string values.
    number_value = StringVar()
    name_value = StringVar()
    email_value = StringVar()
    address_value = StringVar()

    # Trace write changes and send callback to given function.
    number_value.trace_add(mode="write", callback=validate_number)
    name_value.trace_add(mode="write", callback=validate_name)
    email_value.trace_add(mode="write", callback=validate_email)
    address_value.trace_add(mode="write", callback=validate_address)

    entry_options = dict(fg="#808080", width=29, font=("Arial", 11), borderwidth=0)

    name_entry = Entry(entry_frm1, textvariable=name_value, **entry_options)
    number_entry = Entry(entry_frm2, textvariable=number_value, **entry_options)
    email_entry = Entry(entry_frm3, textvariable=email_value, **entry_options)
    address_entry = Entry(entry_frm4, textvariable=address_value, **entry_options)

    name_placeholder = "Full Name"
    number_placeholder = "Number"
    email_placeholder = "Email"
    address_placeholder = "Address"
    
    entries = [name_entry, number_entry, email_entry, address_entry]
    placeholders = [name_placeholder, number_placeholder, email_placeholder, address_placeholder]

    # Loop through entries and placeholders simultaneously
    for _widget, placeholder in zip(entries, placeholders):
        # Place the widget at the specified coordinates
        _widget.place(x=7, y=6)
        # Bind the FocusIn event to call on_focus function with the placeholder as an argument
        _widget.bind("<FocusIn>", lambda e, p=placeholder: on_focus(e, p))
        # Bind the FocusOut event to call on_leave function
        _widget.bind("<FocusOut>", on_leave)
        # Insert the placeholder text into the widget
        _widget.insert(0, placeholder)

    # Check if any of the variables title, number, email, or address have a value
    if any(var for var in [title, number, email, address]):

        # Loop through the widgets, placeholders, and corresponding text values
        for widget_, placeholder, text in zip(entries, placeholders, [title, number, email, address]):
            # Skip if text is equal to the number and it's a string
            if text == str(number):
                continue
            elif text:
                widget_.config(fg="#1f1f1f")  # Configure the widget to display text in black color
                widget_.delete(0, END)  # Clear the widget's contents
                widget_.insert(0, text)  # Insert the provided text into the widget

    name_entry.focus_force()  # Set focus to name_entry immediately.

    button_frame = Frame(
        add_window,
        bg="#fff"
        )
    button_frame.pack(fill=X)

    save_btn = Button(button_frame, image=images[6], cursor="hand2", bg="#77C2FF", activebackground="#5cb3fb", pady=5, width=245, height=30, borderwidth=0, font=("Verdana", 10), command=save_data)
    save_btn.pack(pady=8)
    save_btn.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))  # Change background color when cursor enters the button. 
    save_btn.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))  # Restore background color when cursor leave the button.
    add_window.bind("<Return>", lambda e : save_data())  # Call save_data function when enter key triggered.

def change_frame():
    """
    This function change frame to empty style and contact style,
    if contact_list have no such task it will change to empty style
    otherwise it will change frame to task style.
    """
    contact_count = contact_list.size()  # Get the number (length) of items in the contacts_list widget.
    
    if contact_count == 0:
        contact_list.place_forget()
        empty_contact.place(x=0, y=100)
    else:
        empty_contact.place_forget()
        contact_list.place(x=0, y=40)

def split_character(string) -> str:
    """
    Function to split a string into individual characters.

    Args:
        string (str): The input string to be split.

    Returns:
        str: The string with characters separated by spaces.
    """
    # Strip leading and trailing whitespaces, then remove any newline characters
    string = string.strip().replace("\n", "")

    if len(string) > 24:  # Check if the length of the string is greater than 24 characters
        output_string = ""
        for i in range(0, len(string), 24):  # Iterate over the string in chunks of 24 characters
            # Append each chunk to the output string with a newline character
            output_string += string[i:i+24] + '\n'
        # Return the modified string with chunks separated by newline characters
        return output_string
    # If the length of the string is not greater than 24, return the original string
    return string

def update_list(*args):
    """
    Function to update the contact list based on the search term.
    """
    hide_contact_frame()  # Call hide_contact_frame function
    # Retrieve the names from the list table in the database
    list_data = [row[0] for row in db_cursor.execute('SELECT name FROM list')]

    contact_list.delete(0, END)  # Clear all items from the contact_list

    search_term = search_value.get()  # Get the current value of the search_value StringVar

    # Check if the search_term is empty or equal to the search_placeholder
    if search_term == "" or search_term == search_placeholder:
        # Insert all items from list_data into contact_list
        for item in list_data:
            contact_list.insert(END, item)
    else:
        # Insert items from list_data into contact_list if they contain the search_term
        for item in list_data:
            if search_term.lower() in item.lower():
                contact_list.insert(END, item)

    change_frame()  # Call the change_frame function.

def update_dialog():
    """
    Function to update the dialog box with the selected contact details for editing.
    """
    # Initialize getpass to False
    getpass = False

    try:
        # Get the index of the selected item in contact_list
        index = contact_list.curselection()

        # Check if more than one item is selected
        if len(index) > 1:
            # Display an information message if more than one item is selected
            showinfo("Update contact", "Please select a contact to update!")
        
        # Check if exactly one item is selected
        elif len(index) > 0 and len(index) <= 1:
            getpass = True  # Set getpass to True
        else:
            # Raise an IndexError if no item (contact) is selected
            raise IndexError()

    except Exception:
        # Show a message if no contact is selected
        showinfo("Update contact", "No such contact selected!")

    if getpass:
        data = db_cursor.execute('SELECT * FROM list WHERE id = ?', (index[0],)).fetchone()
        id_, name, number, email, address = data

        add_dialog(
            window_title="Update contact",
            index_id=id_,
            title=name,
            number=number,
            email=email,
            address=address
            )

def delete_contact():
    """
    Function to delete the selected contact from the database.
    """
    try:
        # Get the indices of the selected items in contact_list
        selected_index = contact_list.curselection()

        # Check if no item is selected, raise an IndexError
        if not selected_index:
            raise IndexError()
        
        # Check if more than one item is selected
        if len(selected_index) > 1:
            # Create a message indicating the number of selected contacts
            words = f"{len(selected_index)} contacts"
        else:
            # Create a message for a single selected contact
            words = "This contact"

        # Prompt the user for confirmation to delete the selected contacts
        getpass = askquestion(f"Delete {words.split()[-1]}", f"{words} will be deleted.\nAre you sure ?")
    except Exception:
        # Set getpass to False if an exception occurs
        getpass = False
        # Show a message if no contact is selected
        showinfo("Delete contact", "No such contact selected!")

    if getpass == "yes":
        hide_contact_frame()  # Call hide_contact_frame function

        # Iterate over the selected indices in reversed order
        for index in reversed(selected_index):
            # Delete the corresponding entry from the list table in the database
            db_cursor.execute("delete from list where id = ?", (index,))
            # Delete the entry from the contact_list
            contact_list.delete(index)
        db_connection.commit()  # Commit changes to the database

        contacts = contact_list.get(0, END)  # Get all items from the contact_list
        data = db_cursor.execute('SELECT * FROM list').fetchall()  # Retrieve all data from the list table in the database
        ids = [row[0] for row in data]  # Extract the IDs from the retrieved data

        # Iterate over the contacts list along with their indices
        for index, contact in enumerate(contacts):
            # Update the id of the contact in the list table in the database
            db_cursor.execute("update list set id = ? where id = ?", (index, ids[index]))
            
    db_connection.commit()  # Commit changes to the database
    update_global_data()  # Update global_data with names from database
    change_frame()  # Call the change_frame function.

contact_frame = Frame(root, bg="#fff", width=356, height=555, highlightbackground="#808080", highlightthickness=2)
contact_frame.place(x=22, y=20)

Frame(contact_frame, height=40, width=2, bg="#7baad0").place(x=268, y=0)
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

contact_info_options = dict(
    master=contact_info,
    font=("Roboto", 12),
    compound="left",
    justify="left",
    anchor="w",
    width=290,
    bg="#fff",
    padx=10
    )

contact_number = Label(**contact_info_options, image=images[7])
contact_number.pack(pady=5)

contact_email = Label(**contact_info_options, image=images[8])
contact_email.pack(pady=5)

contact_address = Label(**contact_info_options, image=images[9])
contact_address.pack(pady=5)

frame_line_options = dict(master=detail_frame, height=4, bg="#808080")

frame_line1 = Frame(**frame_line_options, width=160)
frame_line3 = Frame(**frame_line_options, width=280)
frame_line2 = Frame(**frame_line_options, width=280)
frame_line4 = Frame(**frame_line_options, width=280)
frame_line5 = Frame(**frame_line_options, width=280)

frame_lines = [frame_line1, frame_line2, frame_line3, frame_line4, frame_line5]
line_coordinates = [
    dict(x=95, y=160),
    dict(x=35, y=245),
    dict(x=35, y=330),
    dict(x=35, y=415),
    dict(x=35, y=500)
]

# Place each frame in the frame_lines list at its corresponding position
for frame, postion in zip(frame_lines, line_coordinates):
    frame.place(postion)

def show_contact(event=None, getindex=-1):
    """
    Display contact information based on the selected index.

    Args:
        event: The event that triggers the function (default is None).
        getindex: The index of the selected item (default is -1).
    """
    try:
        # Check if getindex is greater than or equal to 0
        if getindex >= 0 :
            # If true, set widget to event and index to getindex
            widget = event
            index = getindex
        else:
            # If false, set widget to event.widget and selected_index to the index of the selected item
            widget = event.widget
            selected_index = widget.curselection()[0]

        # Get the value at the selected index from the widget
        value = widget.get(selected_index)

        # Update global_index to the index of the value in global_data
        global_index = global_data.index(value)

        getpass = True  # Set getpass to True

        contact_title.config(text=value)  # Update the contact title label with the value
    except Exception:
        # Set getpass to False if an exception occurs
        getpass = False  

    if getpass:
        show_contact_frame()  # Call show_contact_frame function to show contacts info.
        # Retrieve the data for the specified id from the list table in the database
        data = db_cursor.execute('SELECT * FROM list WHERE id = ?', (global_index,)).fetchone()
        # Unpack the data into id_, name, number, email, and address variables
        id_, name, number, email, address = data
        # print(id_, name, number, email, address)

        # Update the contact number label with the provided number if available; otherwise, set it to "Add phone number"
        if number:
            contact_number.config(text=number)
        else:
            contact_number.config(text="Add phone number")
            
        # Update the contact email label with the provided email if available; otherwise, set it to "Add email"
        if email:
            contact_email.config(text=email)
        else:
            contact_email.config(text="Add email")

        # Update the contact address label with the provided address if available; otherwise, set it to "Add Address"
        if address:
            contact_address.config(text=address)
        else:
            contact_address.config(text="Add Address")

def show_contact_frame(event=None):
    """
    Hide all frames in the frame_lines list and display the title_frame and contact_info.

    Args:
        event: The event that triggers the function (default is None).
    """
    # Hide all frames in the frame_lines list
    for frame in frame_lines:
        frame.place_forget()

    # Display the title_frame and contact_info
    title_frame.place(x=15, y=145)
    contact_info.place(x=15, y=200)

def hide_contact_frame(event=None):
    """
    Display all frames in the frame_lines list at their respective positions and hide title_frame and contact_info.

    Args:
        event: The event that triggers the function (default is None).
    """
    for frame, postion in zip(frame_lines, line_coordinates):
        frame.place(postion)

    # Hide title_frame and contact_info
    title_frame.place_forget()
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
# contact_list.bind("<FocusOut>", hide_contact_frame)

# Create a StringVar to store the value entered for search
search_value = StringVar()

# Add a trace to the search_value variable to call the update_list function whenever its value is modified
search_value.trace_add(callback=update_list, mode="write")

search_box = Entry(contact_frame, insertbackground="#505050", textvariable=search_value, fg="#505050", width=28, font=("Arial", 12), borderwidth=0)
search_placeholder = "Search contacts"
search_box.insert(0, search_placeholder)

# contact_title.config(textvariable=search_value)

def on_focus(event):
    """
    Function to handle the focus event for the search_box entry widget.

    Args:
        event: The event that triggers the function.
    """
    # Check if the current text in search_box is equal to the search_placeholder
    if search_box.get() == search_placeholder:
        search_box.config(fg="#000")  # Change the text color to black
        search_box.delete(0, END)  # Clear the contents of search_box

def on_leave(event):
    """
    Function to handle the leave event for the search_box entry widget.

    Args:
        event: The event that triggers the function.
    """
    # Check if search_box is empty
    if search_box.get() == "":
        search_box.config(fg="#505050")  # Change the text color to a light gray
        search_box.insert(0, search_placeholder)  # Insert the search_placeholder text into search_box

search_box.bind("<FocusIn>", on_focus)  # Call 'on_focus' function when widget receives focus.
search_box.bind("<FocusOut>", on_leave)  # Call 'on_leave' function when focus leaves the widget.
search_box.place(x=10, y=8)

search_btn = Button(contact_frame, fg="#fff", image=images[2], width=80, height=36,borderwidth=0, bg="#77C2FF", activebackground="#5cb3fb", activeforeground="#fff", pady=6, font=("Verdana", 12))
search_btn.place(x=270, y=0)

# Change search button background color when cursor enters the widget.
search_btn.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))

# Change search button background color when cursor enters the widget.
search_btn.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))

add_btn = Button(contact_frame, command=add_dialog, width=90)
update_btn = Button(contact_frame, command=update_dialog, width=90)
delete_btn = Button(contact_frame, command=delete_contact, width=90)

add_btn.place(x=0, y=502)
update_btn.place(x=118,y=502)
delete_btn.place(x=236, y=502)

btn_text = ["Add", "Update", "Delete"]

for index, widget in enumerate([add_btn, update_btn, delete_btn]):
    widget.config(
        text=btn_text[index],
        font=("Arial", 12),
        cursor="hand2",
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
    
    # Change button background color when cursor enters the widget.
    widget.bind("<Enter>", lambda e : e.widget.config(bg="#5cb3fb"))

    # Restore button background color when cursor leaves the widget.
    widget.bind("<Leave>", lambda e : e.widget.config(bg="#77C2FF"))

root.mainloop()  # Run the tkinter event loop.