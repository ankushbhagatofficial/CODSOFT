from sys import exit

try:
    from tkinter import (
        Tk,
        Frame,
        Label,
        Button,
        Canvas
    )

    from time import sleep
    from PIL import ImageTk
    from pickle import load as pload
    from random import choice as rchoice
    from tkinter.messagebox import showinfo
except ModuleNotFoundError as err:
    print(err)
    exit(1)

moves = ["rock", "paper", "scissors"]
restart = False
cpu_score = 0
my_score = 0

root = Tk()  # Create a tkinter root window.
root.title("Rock Paper Scissors")

window_width = 500
window_height = 350

# Get the screen width and height.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the center coordinates for positioning the window.
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

# Set the geometry of the window to be centered on the screen.
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
root.resizable(0,0)  # Disable window resizing.

frame = Frame(width=420, height=200, borderwidth=2, relief="ridge", bg="#ffed4f")
frame.place(x=35, y=50)

images = []
image_data = pload(open("assets.dat", "rb"))  # Load image data from the "assets.dat" file.

for image in image_data:
    images.append(ImageTk.PhotoImage(image))

def move_image_down(count):
    """
    Function to move an image down recursively.
    """
    if count > 0:
        canvas.move(image_id, 0, 5)  # Move the image down by 5 units.
        canvas.after(50, move_image_down, count - 1)
    else:
        canvas.after(100, move_image_up, 4)  # Move up after 0.1 second, four times

def move_image_up(count):
    """
    Function to move an image up recursively.
    """
    if count > 0:
        canvas.move(image_id, 0, -5)  # Move the image up by 5 units.
        canvas.after(50, move_image_up, count - 1)
    else:
        canvas.after(100, move_image_down, 4)  # Move down after 0.1 second, four times

def animate_hands():
    """
    Function to animate the hands.
    """
    canvas.pack()

    # If restart is not True (False), call the function.
    if not restart:
        move_image_down(4)  # Move down four times initially

def show_result(you, cpu):
    """
    Function to display the result of the game.
    """
    global cpu_score, my_score

    canvas.pack_forget()  # Forget canvas to hide animated hands to displays the result.

    # Dictionary mapping move names to their corresponding images
    result_image = {
        "rock":images[0],
        "paper":images[1],
        "scissors":images[2]
    }

    # Get the images corresponding to the CPU's and player's moves from the result_image dictionary.
    cpu_image = result_image[cpu]
    my_image = result_image[you]

    # Set the images for both cpu_result_image and my_result_image widgets
    cpu_result_image.config(image=cpu_image)
    my_result_image.config(image=my_image)

    # Position both cpu_result_image and my_result_image widgets
    cpu_result_image.place(x=10, y=35)
    my_result_image.place(x=275, y=35)

    # Game logic code section.
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
        cpu_score += 1  # Increment CPU score if "Cpu" is in the result.
    elif "You" in result:
        my_score += 1  # Increment player's score if "You" is in the result.
    score = f"Cpu {cpu_score} | You {my_score}"

    # Sets the config of widgets text.
    cpu_result_text.config(text="Cpu")
    result_text.config(text=result)
    my_result_text.config(text="You")
    score_text.config(text="Scores")
    score_result_text.config(text=score)

    # Sets the positions of widgets.
    cpu_result_text.place(x=50, y=170)
    result_text.place(x=140, y=90)
    my_result_text.place(x=320, y=170)
    score_text.place(x=150, y=145)
    score_result_text.place(x=100, y=170)

    # Sets the button image and their positions.
    retry_image.place(x=196, y=280)
    retry_button.place(x=217, y=288)

def show_hands(move=None):
    """
    Function to show animated hands (loading screen) and send moves to 'show_result' function after 1.2 sec.
    """

    # Call functions to forget images and their text.
    forget_images()
    forget_text()

    # Forget some widgets to clean screen for upcoming result.
    reset_score_image.place_forget()
    reset_score_button.place_forget()
    text.place_forget()
    
    you = move  # Set user move.
    cpu = rchoice(moves)  # Get random choice of move for cpu.

    animate_hands()  # Call animated_hands function before sends choices to 'show_result'.

    # After 1.2 sec, call the show_result function with the 'you' and 'cpu' arguments.
    canvas.after(1200, lambda : show_result(you, cpu))

def change_rock(event=None):
    """
    Function to change the position of the rock image.
    """
    if event:
        # Call default_image_position function when cursor leaves the rock widget.
        rock.bind("<Leave>", default_image_position)
        sleep(0.01)
        rock.place(x=10, y=20)
        sleep(0.1)
    else:
        # Call Nothing when cursor leaves the rock widget.
        rock.bind("<Leave>", lambda e : None)
        sleep(0.2)
        show_hands("rock")

def change_paper(event=None):
    """
    Function to change the position of the paper image.
    """
    if event:
        # Call default_image_position function when cursor leaves the paper widget.
        paper.bind("<Leave>", default_image_position)
        sleep(0.01)
        paper.place(x=140, y=20)
        sleep(0.1)
    else:
        # Call Nothing when cursor leaves the paper widget.
        paper.bind("<Leave>", lambda e : None)
        sleep(0.2)
        show_hands("paper")

def change_scissors(event=None):
    """
    Function to change the position of the scissors image.
    """
    if event:
        # Call default_image_position function when cursor leaves the scissors widget.
        scissors.bind("<Leave>", default_image_position)
        sleep(0.01)
        scissors.place(x=275, y=20)
        sleep(0.1)
    else:
        # Call Nothing when cursor leaves the scissors widget.
        scissors.bind("<Leave>", lambda e : None)
        sleep(0.2)
        show_hands("scissors")

def default_image_position(e=None):
    """
    Function to set the default position of the rock, paper, and scissors images.
    """
    rock.place(x=10, y=35)
    paper.place(x=140, y=35)
    scissors.place(x=275, y=35)

def default_text_position():
    """
    Function to set the default position of the text labels associated with rock, paper, and scissors.
    """
    rock_text.place(x=40, y=165)
    paper_text.place(x=160, y=165)
    scissors_text.place(x=300, y=165)

def forget_images():
    """
    Function to hide the rock, paper, and scissors images.
    """
    rock.place_forget()
    paper.place_forget()
    scissors.place_forget()

def forget_text():
    """
    Function to hide the text labels associated with rock, paper, and scissors.
    """
    rock_text.place_forget()
    paper_text.place_forget()
    scissors_text.place_forget()

def reset_scores():
    """
    Function to reset the scores in a game.
    """
    global cpu_score, my_score
    cpu_score = 0
    my_score = 0
    showinfo("Reset", "Scores has been reset.")

def restart_game():
    """
    Function to restart the game and set all back to initial place.
    """
    global restart
    restart = True

    cpu_result_image.place_forget()
    my_result_image.place_forget()

    cpu_result_text.place_forget()
    result_text.place_forget()
    my_result_text.place_forget()
    score_text.place_forget()
    score_result_text.place_forget()

    retry_image.place_forget()
    retry_button.place_forget()

    reset_score_image.place(x=8, y=305)
    reset_score_button.place(x=20, y=312)
    text.place(x=130, y=260)

    default_image_position()
    default_text_position()

frame_options = dict(master=frame, bg="#ffed4f")
main_options = dict(**frame_options, borderwidth=0, activebackground="#ffed4f")

rock = Button(**main_options, image=images[0], command=lambda : change_rock())
paper = Button(**main_options, image=images[1], command=lambda : change_paper())
scissors = Button(**main_options, image=images[2], command=lambda : change_scissors())
default_image_position()

rock.bind("<Enter>", change_rock)  # Call 'change_rock' function when cursor enters the widget.
paper.bind("<Enter>", change_paper)  # Call 'change_paper' function when cursor enters the widget.
scissors.bind("<Enter>", change_scissors)  # Call 'change_scissors' function when cursor enters the widget.

rock_text = Label(**frame_options, text="Rock", font=("Verdana", 12, "bold"))
paper_text = Label(**frame_options, text="Paper", font=("Verdana", 12, "bold"))
scissors_text = Label(**frame_options, text="Scissors", font=("Verdana", 12, "bold"))
default_text_position()

retry_image =  Label(image=images[4])
retry_button = Button(text="Retry", cursor="hand2", font=("Roboto", 11, "bold"), bg="#ffed4f", activebackground="#ffed4f", borderwidth=0, command=restart_game)

reset_score_image =  Label(image=images[5])
reset_score_button = Button(text="Reset", cursor="hand2", font=("Roboto", 10), fg="#fff", bg="#747474", activeforeground="#ff4949", activebackground="#747474", borderwidth=0, command=reset_scores)
reset_score_image.place(x=8, y=305)
reset_score_button.place(x=20, y=312)

cpu_result_image = Label(**frame_options)
my_result_image = Label(**frame_options)

cpu_result_text = Label(**frame_options, font=("Verdana", 12, "bold"))
result_text = Label(**frame_options, font=("Verdana", 14, "bold"), justify="center", width=10)
score_text = Label(**frame_options, font=("Verdana", 11, "bold"), justify="center", width=10)
score_result_text = Label(**frame_options, font=("Verdana", 11, "bold"), justify="center", width=20)
my_result_text = Label(**frame_options, font=("Verdana", 12, "bold"))

text = Label(text="Make your choice", font=("Verdana", 20))
text.place(x=130, y=260)

canvas = Canvas(frame, bg="#ffed4f", width=420, height=200)
image_id = canvas.create_image(210,90, image=images[3])

root.mainloop()  # Run the tkinter event loop.