from sys import exit

try:
    from tkinter import (
        Tk,
        Frame,
        Label,
        Button,
        IntVar,
        LabelFrame
    )

    from time import sleep
    from tkSliderWidget import Slider
    from tkinter.ttk import Checkbutton
    from random import choice as rchoice
    from string import ascii_uppercase, ascii_lowercase, digits, punctuation
except ModuleNotFoundError as err:
    print(err)
    exit(1)

root = Tk()  # Create a tkinter root window.
root.title("Password Generator")

window_width = 500
window_height = 400

# Get the screen width and height.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center coordinates for positioning the window.
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

# Set the geometry of the window to be centered on the screen.
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
root.resizable(0, 0)  # Disable window resizing.

generated_password = []

def generate_password():
    """
    Function to generate and display passwords.
    """
    global generated_password
    tmp_password = generated_password  # Assign the global varibale 'generated_password' to a 'tmp_password'.
    
    password_length = slider.getValues()  # Get the value of the slider for password length.

    upper = ascii_uppercase  # Uppercase letters
    lower = ascii_lowercase  # Lowercase letters
    numbers = digits  # Numbers
    symbols = punctuation  # Symbols

    isnumbers = chbox_num_value.get()  # Get the value of the checkbox for numbers.
    issymbols = chbox_sym_value.get()  # Get the value of the checkbox for symbols.

    passwords = upper+lower  # Concatenate the uppercase and lowercase letters.
    password_types = [numbers, symbols]  # List of password character types
    checkbox = [isnumbers, issymbols]   # List of checkbox values

    for index, password in enumerate(password_types):
        if checkbox[index] == 1:  # Check if the checkbox for this password type is checked (1).
            passwords += password  # Add the characters of this password type to the available characters for generating passwords.

    generated_password = []
    generated_password_list = []

    for password in range(int(password_length[0])):
        passwd = rchoice(passwords)  # Randomly choose characters from the available characters.
        generated_password_list.append(passwd)  # Append the chosen character to the generated password list.

    # Concatenate the characters in the generated password list to form the final password.
    generated_password = "".join(generated_password_list)

    if len(generated_password) == len(tmp_password):  # If the length of the generated password matches the length of the temporary password.
        # Store each character of the temporary password.
        store_password = [char for char in tmp_password]
        # print(store_password, generated_password_list)

        for index, password in enumerate(generated_password_list):
            store_password[index] = password  # Replace the character at the corresponding index with the generated character.
            password = "".join(store_password)  # Join the characters back into a string.
            sleep(0.00500)  # Pause for a short duration to show text animation.
            password_label.config(text=password)  # Update the password label with the new password.
            root.update()  # Update the tkinter window.
        generated_password = password  # Update the generated password.
    else:
        generated_password = "".join(generated_password_list)  # Concatenate the characters in the generated password list.
        password_label.config(text=generated_password)  # Update the password label with the generated password.

def copy_password():
    """
    Function to copy the generated password to the clipboard.
    """
    if generated_password:
        root.clipboard_clear()  # Clear the contents of the clipboard in tkinter.
        root.clipboard_append(generated_password)  # Append the generated password to the clipboard in tkinter.
        root.update()  # Update the tkinter window to set the copied passwords to the system clipboard.

Label(text="Password Generator", font=("Verdana", 24), fg="#3d3d3d").pack(pady=10)
# Frame(width=325, height=2, bg="#3d3d3d").pack()

main_frame = Frame(width=450, height=300, relief="ridge", borderwidth=4)
main_frame.place(x=25, y=70)

password_frame = Frame(main_frame, width=330, height=40, borderwidth=2, relief="ridge", bg="#e4e4e4")
password_frame.place(x=15, y=15)

password_label = Label(password_frame, text="No Password Generated", font=("Verdana", 10), justify="left", bg="#e4e4e4")
password_label.place(x=10, y=7)

copy_button = Button(main_frame, cursor="hand2", width=6, text="Copy", borderwidth=2, relief="ridge", command=copy_password, bg="#77C2FF", activebackground="#77C2FF", font=("Verdana", 11), padx=10, pady=5)
copy_button.place(x=350, y=15)

slider_frame = LabelFrame(main_frame, text="Length: 8", width=415, height=70, borderwidth=2, relief="ridge", font=("Verdana", 10))
slider_frame.place(x=15, y=90)

Label(slider_frame, text="Password length (8-32)", font=("Verdana", 8)).place(x=2, y=11)

slider = Slider(slider_frame, width = 240, height = 40, min_val = 8, max_val = 32, show_value = True)
slider.place(x=168, y=5)

# Get realtime callback values from slider widget when it moves and sets to 'slider_frame' text.
slider.setValueChangeCallback(lambda vals : slider_frame.config(text=f"Length: {vals[0]}"))

# Set variables to store integer values.
chbox_num_value = IntVar()
chbox_sym_value = IntVar()

# Set value 1 to variables to make checkbutton as checked.
chbox_num_value.set(1)
chbox_sym_value.set(1)

chbox_sym = Checkbutton(main_frame, text="Include Symbols", variable=chbox_sym_value, takefocus=False)
chbox_num = Checkbutton(main_frame, text="Include Numbers", variable=chbox_num_value, takefocus=False)

chbox_num.place(x=60, y=190)
chbox_sym.place(x=270, y=190)

button = Button(main_frame, cursor="hand2", text="Generate", width=30, borderwidth=2, relief="ridge", command=generate_password, bg="#77C2FF", activebackground="#77C2FF", font=("Verdana", 12), padx=10, pady=5)
button.place(x=56, y=236)

root.mainloop()  # Run the tkinter event loop.