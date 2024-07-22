from tkinter import *
import pandas as pd
from random import randint

BACKGROUND_COLOR = "#B1DDC6"

filename = "data/french_words.csv"
df = pd.read_csv(filename)
rows = df.shape[0]
# keep track of the words that are already seen in one session
appeared_word = [False] * rows
# made global in order to access it in 'good_answer' function
current_index = None


def remove_word(index):
    file_path = "data/remaining_words.csv"
    data = pd.read_csv(file_path)
    data = data.drop(index)
    data.to_csv(file_path, index=False)


def fill_remaining_words():
    global appeared_word
    appeared_word = [False] * rows
    source_file = "data/french_words.csv"
    destination_file = "data/remaining_words.csv"
    # copy words from 'french_words' to 'remaining_words'
    words = pd.read_csv(source_file)
    words.to_csv(destination_file, index=False)


def show_new_word():
    global current_index
    current_index = randint(0, rows - 1)
    while appeared_word[current_index]:
        current_index = randint(0, rows - 1)
    appeared_word[current_index] = True
    french_word = df.iloc[current_index, 0]
    canvas.itemconfig(word, text=french_word)
    canvas.itemconfig(current_language, text="French")
    canvas.itemconfig(card_image, image=card_front_img)
    window.after(3000, flip_card, current_index)


def flip_card(index):
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(current_language, text="English")
    english_word = df.iloc[index, 1]  # get the english word
    canvas.itemconfig(word, text=english_word)


def wrong_answer():
    show_new_word()


def good_answer():
    show_new_word()
    remove_word(current_index)


window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)

current_language = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

# Buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, borderwidth=0, command=wrong_answer)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, borderwidth=0, command=good_answer)
known_button.grid(row=1, column=1)

fill_remaining_words()
show_new_word()
window.mainloop()
