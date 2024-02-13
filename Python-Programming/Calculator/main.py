from sys import exit

try:
    from tkinter import (
        Tk,
        Frame,
        Label,
        Button,
        StringVar
    )

    from time import sleep
except ModuleNotFoundError as err:
    print(err)
    exit(1)

root = Tk()  # Create a tkinter root window.
root.title("Calculator")

window_width = 450
window_height = 540

# Get the screen width and height.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center coordinates for positioning the window.
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

# Set the geometry of the window to be centered on the screen.
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

root.config(bg="#fff")  # Set the main window background color to white.
root.resizable(0,0)  # Disable window resizing.

values = ""
error = False
clear_result = False
numbers = str(list(range(10)))
operators = ["−", "-", "×", "%", "÷", "+", "/", "*", "."]

def erase(event=None):
    """
    Remove the last character from values or an empty string if the values is 0 and show it to result frame.

    Args:
        event (Tkinter.Event, optional): The event object representing the key press event. Defaults to None.

    Example:
        >>> erase("100-20/40")
        "100-20/4"
    """
    global values
    result_label.config(fg="#000")  # Set widget foreground color to black.
    if values == "Error":  # If the value is "Error", set the global variable 'values' to an empty string.
        values = ""

    values = values[:len(values)-1]  # Remove the last character from the global variable 'values'.
    value = values

    if not values:  # If global variable 'values' is empty, set 'value' to string 0 and call a function.
        value = "0"
        hide_pre_result()

    try:
        presult = calculate(values)  # Get calculated values of global variable 'values'.
        pre_result.set(presult)  # Set string values to 'pre_result'.
    except Exception:
        # Count the occurrences of operators in the 'value' string
        opr_count = sum(1 for char in value if char in operators)

        if opr_count == 1:  # If 'opr_count' is equal to 1, call the 'hide_pre_result' function.
            hide_pre_result()
        pre_result.set(value)  # Set string values to 'pre_result'.

    result_label.config(text=value)  # Set text of the widget to value.

def clear(event=None):
    """
    Clear the result frame output and reset 'values'global variable to 0.

    Args:
        event (Tkinter.Event, optional): The event object representing the key press event. Defaults to None.
    """
    global values, clear_result
    values = ""  # Set global variable 'values' to empty string.
    hide_pre_result()
    pre_result.set("")  # Set empty string to 'pre_result'.
    clear_result = False
    result_label.config(fg="#000")  # Set widget foreground color to white.
    result_label.config(text="0")  # Set the text of the widget to "0".

def show_values(value=None, event=None):
    global values, error, clear_result
    result_label.config(fg="#000")  # Set widget foreground color to white.
    if event:
        kvalue = event.keysym # Assign the keysym (name of the key) from the event to kvalue.
        if kvalue == "Escape":
            clear()
        elif kvalue.lower() == "q": # If kvalue equals to 'q' or 'Q', close the root window after 0.2 sec.
            sleep(0.2)
            root.destroy()

        evalue = event.char  # Assign the character input from the event to evalue.
        # Check if evalue in numbers or contains any of the specified operators or symbols.
        if evalue in numbers or evalue in ["%", "/", "x", "*", "-", "+", "."]:
            if evalue:
                # Replace certain operators with their respective symbols
                for x, y in zip(["/", "x", "*"], ["÷", "×", "×"]):
                    evalue = evalue.replace(x, y)
                value = evalue
    if value:
        if len(values) < 16:  # Checks if global variable 'values' length is less than 16.
            values += value
            result = values
        else:
            result_label.config(fg="#ff6060")  # Set widget foreground color to red.
            result = values
        try:
            # If clear_result is True and the value contains only of numbers.
            if clear_result and int(value):
                values = value
                result = value
                clear_result = False
        except Exception:
            clear_result = False
            # If there's an error is True and the last character of the value is not an operator.
            if error and not value[-1] in operators:
                error = False
                values = value
                result = value

        try:
            values = filter_duplicate_operators(values)  # Remove duplicate operators from values.
            result = values
        except Exception:
            pass

        try:
            presult = calculate(values)  # Get calculated values of global variable 'values'.
            if pre_result.get()[-1] in operators:  # If the last character of the 'pre_result' is an operator, call 'show_pre_result' function.
                show_pre_result()
            pre_result.set(presult)  # Set string values to 'pre_result'.
        except Exception:
            presult = values
            pre_result.set(presult)  # Set string values to 'pre_result'.

        result_label.config(text=result)  # Set text of the widget to result.


def filter_duplicate_operators(value:str):
    """
    Removes consecutive duplicate operators from a given string.

    Parameters:
        value (str): The input string containing operators.

    Returns:
        str: A string with consecutive duplicate operators removed.
    """
    last_value = value[-1]  # Get the last value of 'value'.
    second_last_value = value[-2]  # Get the second last value of 'value'.

    if second_last_value in operators:  # Checks if 'second_last_value' in 'operators'.
        for symbol in operators:
            if symbol == last_value:  # Checks if 'symbol' equals to 'last_value'.
                # print(values)
                value = value[:-1]  # Get the last value of 'value'.
                value = value.replace(second_last_value, last_value)  # Replace 'second_last_value' with 'last_value'.
                # print(values)
                return value
    return value


def filter_operators(value:str):
    """
    Replace special mathematical operators with their standard equivalents in the given expression.

    Args:
        value (str): The mathematical expression possibly containing special operators.

    Returns:
        str: The expression with special operators replaced by their standard equivalents.

    Examples:
        >>> filter_operators('5−2×3÷4')
        '5-2*3/4'
    """
    # Replace special mathematical symbols (x) with their corresponding operators (y) in the expression (value).
    for x, y in zip(["−", "×", "÷"], ["-", "*", "/"]):
        if x in value:
            value = value.replace(x, y)
    return value


def filter_decimals(value:str):
    """
    Filter decimal values in the given expression.

    Args:
        value (float): The numerical value to be filtered.

    Returns:
        str: The filtered numerical value as a string.

    Examples:
        >>> filter_decimals(3.0)
        '3'
        >>> filter_decimals(3.141592653589793)
        '3.1416'
    """
    if str(value).endswith(".0"):  # If the value ends with ".0", convert it to an integer and then to a string. 
        result = str(int(value))
    else:
        result = str(round(value, 4))  # Round the value to 4 decimal places and convert it to a string.
    return result


def filter_percentage(expression:str):
    """
    Expand a mathematical expression string by replacing the percentage symbol
    with "/100*" and adding parentheses to ensure proper evaluation.

    Parameters:
        expression (str): A string representing a mathematical expression.

    Returns:
        str: The expanded mathematical expression string.

    Example:
        >>> filter_percentage("100*2%50*2")
        '((100*2)/100*50*2)'

        >>> filter_percentage("100%50")
        '(100/100)*(50)'
    """
    if "%" in expression:
        # Replace the percentage symbol with "/100*"
        expression = expression.replace('%', '/100*')
        
        operators = ["/", "*", "-", "+"]
        for operator in operators:
            if operator in expression:
                # Replace each occurrence of "operator" with ")operator("
                expression = expression.replace(operator, f'){operator}(')
        
        # Add parentheses at the beginning and end of the expression
        expression = '(' + expression + ')'
    
    return expression


def calculate(value:str):
    """
    Calculate the result of the given mathematical expression.

    Args:
        value (str): The mathematical expression to be evaluated.

    Returns:
        str: The result of the evaluation.
    """

    # Apply filters to handle special operators and percentage expressions
    value = filter_operators(value)
    value = filter_percentage(value)

    # Evaluate the expression
    result = eval(value)

    # Filter the resulting value for decimals
    result = filter_decimals(result)

    return result


def show_output(event=None):
    hide_pre_result()
    global values, error, clear_result
    result_label.config(fg="#000")
    result = "0"
    if values:
        # If the first character of global variable 'values' is not in the specified operators.
        if not values[0] in ["*", "/", "×", "÷", "%", "+"]:
            try:
                result = calculate(values)
                values = str(result)
                clear_result = True
            except Exception:
                error = True
                values = ""  # Set global variable 'values' to empty string.
                result = "Error"
                result_label.config(fg="#ff6060")  # Set widget foreground color to red.
        else:
            values = ""  # Set global variable 'values' to empty string.
            clear_result = True
            result = "Format error"
            result_label.config(fg="#ff6060")  # Set widget foreground color to red.
    if result == "0":  # If result equal to string 0, set global variable 'values' to empty string.
        values = ""
    result_label.config(text=result)  # Set text of the widget to result.

def show_pre_result():
    result_label.config(font=("Segoe UI", 30), width=19, pady=0)
    pre_result_label.place(x=10, y=50)

def hide_pre_result():
    pre_result_label.place_forget()
    result_label.config(**result_lable_options)

# Result and it's frame code section.

result_frame = Frame(root, bg="#f3f3f3", highlightthickness=1, highlightbackground="#828282", width=426, height=100)
result_frame.pack(pady=3)

result_lable_options = dict(font=("Segoe UI", 35), width=16, pady=12)

result_label = Label(result_frame, text="0", anchor="e", bg="#f3f3f3", **result_lable_options)
result_label.place(x=0, y=0)

pre_result = StringVar()  # Create StringVar object to store string value.
pre_result_label = Label(result_frame, textvariable=pre_result, font=("Segoe UI", 20), bg="#f3f3f3", anchor="e", width=27)

# Buttons and it's frame code section.

main_frame = Frame(root, width=440, height=430, bg="#fff")
main_frame.pack()

x_button = [6, 114, 222, 331]
y_button = [5, 90, 175, 260, 345]

buttons = [
    "C", "%", "÷", "×",
    "7", "8", "9", "−",
    "4", "5", "6", "+",
    "1", "2", "3", "=",
    "0", ".", "⌫"
]

row = 0
column = 0
number_color = "#f3f3f3"
operator_color = "#c9dbff"

button_options = dict(
    master=main_frame,
    font=("aria", 30),
    width=4,
    relief="ridge"
    )

for index, button in enumerate(buttons):
    if column > 3:  # Reset column to 0 if it greater than 3
        column = 0

    if index%4 == 0 and index != 0:  # Increment row by 1 if index is a multiple of 4 and not equal to 0
        row += 1
        # print("")
        
    # print(button, end=" ")
        
    if button in operators and not button == ".":  # Checks if button in operators and button not equal to '.'
        bgcolor = operator_color  # Set bgcolor to toperator_color.
    else:
        bgcolor = number_color   # Set bgcolor to number_color.

    if row == 0 and column == 0:
        Button(**button_options, text="C", bg="#ffb1f8", activebackground="#fc97f4", command=clear).place(x=x_button[column], y=y_button[row])

    elif row == 3 and column == 3:
        Button(main_frame, text=button, bg="#8cb2ff", activebackground="#76a4fe", font=("aria", 29), width=4, height=3, relief="ridge", command=show_output).place(x=x_button[column], y=y_button[row])
        
    elif row == 4 and column == 2:
        Button(**button_options, text="⌫", activebackground="#eaeaea", command=erase).place(x=x_button[column], y=y_button[row])  # ⋅

    elif button.isdigit() or button == ".":  # Checks if button is contain an number and button not equal to '.'
        Button(**button_options, activebackground="#eaeaea", text=button, bg=bgcolor, command=lambda btn=button : show_values(btn)).place(x=x_button[column], y=y_button[row])
    else:
        Button(**button_options, activebackground="#b4cdff", text=button, bg=bgcolor, command=lambda btn=button : show_values(btn)).place(x=x_button[column], y=y_button[row])
    column += 1  # Increment column by 1.

'''
Bind the "<Delete>" event to the 'clear' function
Call 'clear' function when escape key triggered.
'''
root.bind("<Delete>", clear)

'''
Bind the "<BackSpace>" event to the 'erase' function
Call 'erase' function when backspace key triggered.
'''
root.bind("<BackSpace>", erase)

'''
Bind the "<Return>" event to the show_output function
Call 'show_output' function when enter key triggered.
'''
root.bind("<Return>", show_output)

'''
Bind the "<Key>" event to the show_values function
Call 'show_values' function when any key triggered.
'''
root.bind("<Key>", lambda e : show_values(None, e)) 

root.mainloop()  # Run the tkinter event loop.