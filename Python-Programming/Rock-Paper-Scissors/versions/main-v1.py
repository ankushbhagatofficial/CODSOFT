from time import time
from tkinter import *
from time import sleep
from PIL import Image, ImageTk
from tkinter import messagebox
import random

moves = ["rock", "paper", "scissors"]
restart = False
cpu_score = 0
my_score = 0

image_path = ["images/rock.png", "images/paper.png", "images/scissors.png"]

images = []

root = Tk()
root.title("Rock Paper Scissors")

window_width = 500
window_height = 350

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

root.resizable(0,0)

frame = Frame(width=420, height=200, borderwidth=2, relief="ridge", bg="#ffed4f")
frame.place(x=35, y=50)

image = Image.open("images/hands.png")
resize = image.resize((356, 130))
imagex = ImageTk.PhotoImage(resize)

def change_position(e):
    print(e.x, e.y)
    if e.x < 140:
        rock.place(x=10, y=20)
        scissors.place(x=275, y=40)
        paper.place(x=140, y=40)
    elif e.x < 275:
        paper.place(x=140, y=20)
        rock.place(x=10, y=40)
        scissors.place(x=275, y=40)
    else:
        scissors.place(x=275, y=20)
        paper.place(x=140, y=40)
        rock.place(x=10, y=40)

def move_image_down(count):
    if count > 0:
        canvas.move(image_id, 0, 5)
        canvas.after(50, move_image_down, count - 1)
    else:
        canvas.after(100, move_image_up, 4)  # Move up after 0.1 second, four times

def move_image_up(count):
    if count > 0:
        canvas.move(image_id, 0, -5)
        canvas.after(50, move_image_up, count - 1)
    else:
        canvas.after(100, move_image_down, 4)  # Move down after 0.1 second, four times

def animate_hands():
    canvas.pack()
    
    if not restart:
        move_image_down(4)  # Move down four times initially

def show_result(you, cpu):
    global cpu_score, my_score

    canvas.pack_forget()
    result_image = {
        "rock":images[0],
        "paper":images[1],
        "scissors":images[-1]
    }

    cpu_image = result_image[cpu]
    my_image = result_image[you]

    cpu_result_image.config(image=cpu_image)
    my_result_image.config(image=my_image)

    cpu_result_image.place(x=10, y=35)
    my_result_image.place(x=275, y=35)

    if cpu == "rock" and you == "scissors":
        result = "Cpu Win"
    elif cpu == "paper" and you == "rock":
        result = "Cpu Win"
    elif cpu == "scissors" and you == "paper":
        result = "Cpu Win"
    elif cpu == you:
        result = "Match Draw"
    else:
        result = "You Win"
    
    if "Cpu" in result:
        cpu_score += 1
    elif "You" in result:
        my_score += 1

    score = f"Cpu {cpu_score} | You {my_score}"

    cpu_result_text.config(text="Cpu")
    result_text.config(text=result)
    my_result_text.config(text="You")
    score_text.config(text="Scores")
    score_result_text.config(text=score)

    cpu_result_text.place(x=50, y=170)
    result_text.place(x=140, y=90)
    my_result_text.place(x=320, y=170)
    score_text.place(x=150, y=145)
    score_result_text.place(x=100, y=170)

    restart_image.place(x=196, y=280)
    restart_button.place(x=214, y=291)

def show_hands(move=None):
    forget_images()
    forget_text()
    reset_score_image.place_forget()
    reset_score_button.place_forget()
    text.place_forget()
    you = move
    cpu = random.choice(moves)

    animate_hands()
    
    canvas.after(1200, lambda : show_result(you, cpu))

def change_rock(event=None):
    if event:
        rock.bind("<Leave>", default_image_position)
        sleep(0.01)
        rock.place(x=10, y=20)
        sleep(0.1)
    else:
        rock.bind("<Leave>", lambda e : None)
        sleep(0.2)
        show_hands("rock")
        # rock.after(1000, lambda value="rock" : show_hands(value))

def change_papper(event=None):
    if event:
        paper.bind("<Leave>", default_image_position)
        sleep(0.01)
        paper.place(x=140, y=20)
        sleep(0.1)
    else:
        paper.bind("<Leave>", lambda e : None)
        sleep(0.2)
        show_hands("paper")
        # papper.after(1000, lambda value="papper" : show_hands(value))

def change_scissors(event=None):
    if event:
        scissors.bind("<Leave>", default_image_position)
        sleep(0.01)
        scissors.place(x=275, y=20)
        sleep(0.1)
    else:
        scissors.bind("<Leave>", lambda e : None)
        sleep(0.2)
        show_hands("scissors")
        # scissors.after(1000, lambda value="scissors" : show_hands(value))

for index, image in enumerate(image_path):
    image = Image.open(image)
    resize = image.resize((130, 120))
    images.append(ImageTk.PhotoImage(resize))

def default_image_position(e=None):
    rock.place(x=10, y=35)
    paper.place(x=140, y=35)
    scissors.place(x=275, y=35)

def default_text_position():
    rock_text.place(x=40, y=165)
    paper_text.place(x=160, y=165)
    scissors_text.place(x=300, y=165)

def forget_images():
    rock.place_forget()
    paper.place_forget()
    scissors.place_forget()

def forget_text():
    rock_text.place_forget()
    paper_text.place_forget()
    scissors_text.place_forget()

def reset_scores():
    global cpu_score, my_score
    cpu_score = 0
    my_score = 0
    messagebox.showinfo("Reset", "Scores has been reset.")

def restart_game():
    global restart
    restart = True

    cpu_result_image.place_forget()
    my_result_image.place_forget()

    cpu_result_text.place_forget()
    result_text.place_forget()
    my_result_text.place_forget()
    score_text.place_forget()
    score_result_text.place_forget()

    restart_image.place_forget()
    restart_button.place_forget()

    reset_score_image.place(x=8, y=305)
    reset_score_button.place(x=20, y=312)
    text.place(x=130, y=260)

    default_image_position()
    default_text_position()

rock = Button(frame, image=images[0], borderwidth=0, command=lambda : change_rock(), bg="#ffed4f", activebackground="#ffed4f")
paper = Button(frame, image=images[1], borderwidth=0, command=lambda : change_papper(), bg="#ffed4f", activebackground="#ffed4f")
scissors = Button(frame, image=images[-1], borderwidth=0, command=lambda : change_scissors(), bg="#ffed4f", activebackground="#ffed4f")
default_image_position()

rock_text = Label(frame, text="Rock", font=("Verdana", 12, "bold"), bg="#ffed4f")
paper_text = Label(frame, text="Paper", font=("Verdana", 12, "bold"), bg="#ffed4f")
scissors_text = Label(frame, text="Scissors", font=("Verdana", 12, "bold"), bg="#ffed4f")
default_text_position()

button_path = ["images/btn-yellow.png", "images/btn-grey.png"]
resize_button = [
    (95, 44),
    (60, 32)
]
button_images = []

for index, image in enumerate(button_path):
    image = Image.open(image)
    x, y = resize_button[index]
    resize = image.resize((x, y))
    button_images.append(ImageTk.PhotoImage(resize))

restart_image =  Label(image=button_images[0])
restart_button = Button(text="Restart", font=("Roboto", 11, "bold"), bg="#ffed4f", activebackground="#ffed4f", borderwidth=0, command=restart_game)

reset_score_image =  Label(image=button_images[1])
reset_score_button = Button(text="Reset", font=("Roboto", 10), fg="#fff", bg="#747474", activeforeground="#ff4949", activebackground="#747474", borderwidth=0, command=reset_scores)
reset_score_image.place(x=8, y=305)
reset_score_button.place(x=20, y=312)

rock.bind("<Enter>", change_rock)
paper.bind("<Enter>", change_papper)
scissors.bind("<Enter>", change_scissors)

# frame.bind("<Motion>", change_position)

cpu_result_image = Label(frame, bg="#ffed4f")
my_result_image = Label(frame, bg="#ffed4f")

cpu_result_text = Label(frame, font=("Verdana", 12, "bold"), bg="#ffed4f")
result_text = Label(frame, font=("Verdana", 14, "bold"), bg="#ffed4f", justify="center", width=10)
score_text = Label(frame, font=("Verdana", 11, "bold"), bg="#ffed4f", justify="center", width=10)
score_result_text = Label(frame, font=("Verdana", 11, "bold"), bg="#ffed4f", justify="center", width=20)
my_result_text = Label(frame, font=("Verdana", 12, "bold"), bg="#ffed4f")

text = Label(text="Make your choice", font=("Verdana", 20))
text.place(x=130, y=260)

canvas = Canvas(frame, bg="#ffed4f", width=420, height=200)
image_id = canvas.create_image(210,90, image=imagex)

root.mainloop()
