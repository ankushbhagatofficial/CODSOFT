from tkinter import *

root = Tk()
root.title("Calculator")

window_width = 450
window_height = 520

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

root.config(bg="#fff")
root.resizable(0,0)

values = ""
oncalculate = False
numbers = str(list(range(10)))
operators = ["−","-", "×", "%", "÷", "+", "/", "*", "."]

def erase():
    global values
    result_label.config(fg="#000")
    if values == "Error":
        values = ""

    values = values[:len(values)-1]
    value = values

    if not values:
        value = "0"
    result_label.config(text=value)

def clear():
    global values, oncalculate
    values = ""
    oncalculate = False
    result_label.config(fg="#000")
    result_label.config(text="0")

def show(value=None, event=None):
    global values, oncalculate
    result_label.config(fg="#000")
    if event:
        if event.keysym == "Escape":
            clear()
        elif event.keysym.lower() == "q":
            from time import sleep
            sleep(0.2)
            root.destroy()

        evalue = event.char
        if evalue in numbers or evalue in operators:
            if evalue:
                value = evalue
    if value:
        if len(values) < 18:
            values += value
            result = values
        else:
            result_label.config(fg="#ff6060")
            result = values
        try:
            if oncalculate and int(value):
                oncalculate = False
                values = ""
                result = "0"
        except Exception:
            oncalculate = False

        try:
            last_value = values[-1]
            second_last_value = values[-2]

            if second_last_value in operators:
                for symbol in operators:
                    if symbol == last_value:
                        # print(values)
                        values = values[:-1]
                        values = values.replace(second_last_value, last_value)
                        # print(values)
                        result = values

            # if second_last_value == value and not value in numbers:
            #     values = values[:-1]
            #     result = values

        except Exception:
            pass
        # formated_result = str(f"{int(result):,.0f}")
        result_label.config(text=result)

def calculate():
    global values, oncalculate
    result_label.config(fg="#000")
    result = "0"
    if values:
        if not values[0] in ["*", "/", "×", "÷", "%", "+"]:
            for x, y in zip(["−", "×", "÷"], ["-", "*", "/"]):
                if x in values:
                    values = values.replace(x, y)
            try:
                last_value = values[-1]
                # second_last_value = values[-2]
                # if last_value in numbers and second_last_value in operators:

                if "%" in values:
                    percent_values = values.split("%")
                    exp = ["*", "/", "+", "-"]
                    new_values = []

                    for index, vals in enumerate(percent_values):
                        # Check if index is 0 and any operator is not present in the expression
                        if not index == 0 and not any(operator in vals for operator in exp):
                            new_values.append("*"+str(int(vals)/100))
                        else:
                                new_values.append(vals)
                    values = "".join(new_values)

                # print(values)
                    
                result = eval(values)  # Perform the calculations.
                result = str(int(result))  # Convert float values to interger.
                # else:
                #     result = "Format error"
                #     result_label.config(fg="#ff6060")
            except Exception:
                values = ""
                result = "Error"
                result_label.config(fg="#ff6060")
            values = str(result)
            oncalculate = True
        else:
            values = ""
            result = "Format error"
            result_label.config(fg="#ff6060")
            oncalculate = True
    if result == "0":
        values = ""
    result_label.config(text=result)

result_frame = Frame(root, borderwidth=5, relief="ridge", bg="#d0d6e7")
result_frame.pack(pady=5)

result_label = Label(result_frame, text="0", font=("Segoe UI", 30), bg="#d0d6e7", anchor="e", width=19)
result_label.pack(pady=3)

main_frame = Frame(root, width=440, height=430, bg="#fff")
main_frame.pack()

x_button = [6, 114, 222, 331]
y_button = [5, 90, 175, 260, 345]

# for index_y, y in enumerate(y_button):
#     for index_x, x in enumerate(x_button):
#         if index_x == 3 and index_y == 4:
#             break
#         print(x, y)

Button(main_frame, text="C", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#ffb1f8", command=clear).place(x=6, y=5)
Button(main_frame, text="%", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#a1bbff", command=lambda : show("%")).place(x=114, y=5)
Button(main_frame, text="÷", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#a1bbff", command=lambda : show("÷")).place(x=222, y=5)
Button(main_frame, text="×", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#a1bbff", command=lambda : show("×")).place(x=331, y=5)
Button(main_frame, text="7", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("7")).place(x=6, y=90)
Button(main_frame, text="8", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("8")).place(x=114, y=90)
Button(main_frame, text="9", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("9")).place(x=222, y=90)
Button(main_frame, text="−", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#a1bbff", command=lambda : show("-")).place(x=331, y=90)
Button(main_frame, text="4", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("4")).place(x=6, y=175)
Button(main_frame, text="5", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("5")).place(x=114, y=175)
Button(main_frame, text="6", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("6")).place(x=222, y=175)
Button(main_frame, text="+", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#a1bbff", command=lambda : show("+")).place(x=331, y=175)
Button(main_frame, text="1", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("1")).place(x=6, y=260)
Button(main_frame, text="2", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("2")).place(x=114, y=260)
Button(main_frame, text="3", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("3")).place(x=222, y=260)
Button(main_frame, text="=", font=("aria", 29), width=4, height=3, borderwidth=2, relief="ridge", bg="#7fa2fa", command=calculate).place(x=331, y=258)
Button(main_frame, text="0", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show("0")).place(x=6, y=345)
Button(main_frame, text=".", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=lambda : show(".")).place(x=114, y=345)

Button(main_frame, text="⌫", font=("aria", 30), width=4, borderwidth=2, relief="ridge", bg="#e0e0e0", command=erase).place(x=222, y=345)  # ⋅

root.bind("<Key>", lambda e : show(None, e))
root.bind("<Return>", lambda e : calculate())
root.bind("<BackSpace>", lambda e : erase())
root.bind("<Delete>", lambda e : clear())
root.mainloop()