"""This program was created in Repl.it (https://replit.com/). Thus, all file paths and features were tested there.
To test this code, please transfer the code into the Repl.it IDE for all functionalities to be the same.

Dependencies: The Tkinter library, Random library, audio from the Replit API, the urllib library, AudioSegment from
pydub, and os must be imported before the start of the program. """

# https://docs.python.org/3/library/os.path.html
# Library can be found here:
# https://github.com/python/cpython/blob/3.9/Lib/os.py
import os
# https://docs.python.org/3/library/random.html
# Source Code for the Random library: 
# https://github.com/python/cpython/blob/3.9/Lib/random.py
import random
# https://docs.python.org/3/library/tkinter.html
# written by Fredrik Lundh
import tkinter as tk
# https://docs.python.org/3/library/urllib.html
# Github repository for the source code can be found here:
# https://github.com/python/cpython/tree/3.9/Lib/urllib/
from urllib import request

# Source code and who created the project can be found on Github: 
# https://github.com/jiaaro/pydub
# Pydub is maintained by James Robert, as seen on this site: 
# https://pypi.org/project/pydub/
from pydub import AudioSegment
# https://docs.replit.com/repls/audio
# Used the repl.it API to play audio.
# Created by replit
from replit import audio

# words are a mix of those taken from 
# https://www.3plearning.com/blog/spelling-bee-words-list/ by Jackson Best,
# https://www.spelling-words-well.com/8th-grade-spelling-words.html by Ann 
# Richmond Fisher, and
# https://grammar.yourdictionary.com/spelling-and-word-lists/high-school
# -level-spelling-words.html by Michele Meleen.
# only the data was taken from the outside source in order to provide students 
# with the best learning material,
# but the lists were created by me.

# words used for Level 1
easy_words = [
   'taken', 'cannot', 'stay', 'denim', 'doctor', 'glove', 'ocean', 'cadet',
   'oxen', 'guard', 'horse', 'lamb', 'wrap', 'wreck', 'pitch'
]

# words used for Level 2
middle_words = [
   'chaperone', 'charade', 'whirligig', 'chivalry', 'machinery', 'peasant',
   'perimeter', 'persuade', 'accommodate', 'abstain', 'accumulate', 'dilemma',
   'disbursement', 'discernible', 'discrepancy'
]

# words used for Level 3
difficult_words = [
   'absolve', 'balsamic', 'canoeing', 'dichotomy', 'egomaniacal',
   'frugivorous', 'gregariously', 'historical', 'kinkajou', 'licensure',
   'organism', 'million', 'ambient', 'bracket', 'caterpillar'
]

# returns a new list with 10 randomly selected words
easy_words = random.sample(easy_words, 10)
middle_words = random.sample(middle_words, 10)
difficult_words = random.sample(difficult_words, 10)


# The class, WrappingLabel, is from 
# https://stackoverflow.com/questions/62485520/how-to-wrap-the-text-in-a-
# tkinter-label-dynamically. Credit to @rmb who posted this on Jun 20 2020 at 
# 12:09. This class was the only aspect taken
# from an outside source. All other code is written by me and is my original 
# thoughts.
class WrappingLabel(tk.Label):
   '''a type of Label that automatically adjusts the wrap to the size'''

   def __init__(self, master=None, **kwargs):
       tk.Label.__init__(self, master, **kwargs)
       self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))


class Game():
   def __init__(self):
       # creates the window
       self.root = tk.Tk()
       self.mistakes = []
       self.button_l1_clicked = False
       self.button_l2_clicked = False
       self.button_l3_clicked = False
       self.button_forward = False
       self.button_check_answer = False
       self.check_text = None
       self.word_index = 0
       self.page_number = 1
       self.root.title("SpellNow!")
       # sets the background color with the appropriate hex color code
       self.root.configure(bg='#91EA8B')
       # sets the size of the window
       self.root.geometry("720x500")

   # pronounces the word when the user clicks the "Pronounce it!" button
   def pronounce_word(self):
       if self.button_l1_clicked:
           # checking if the index is in the range of the list
           if self.word_index < len(easy_words):
               file_name_e = easy_words[self.word_index] + '.wav'
               audio.play_file(file_name_e)
       elif self.button_l2_clicked:
           if self.word_index < len(middle_words):
               file_name_m = middle_words[self.word_index] + '.wav'
               audio.play_file(file_name_m)
       else:
           if self.word_index < len(difficult_words):
               file_name_d = difficult_words[self.word_index] + '.wav'
               audio.play_file(file_name_d)

   # checks to see if the answer is correct or not
   def check_answer(self, inp):
       get_user_input = inp.get()
       # creates the label for the output
       self.check_text = tk.Label(self.root, text="", font="Times 16", bg="#91EA8B")
       self.check_text.place(x=200, y=300, height=40, width=200)
       # checking if the user is playing Level 1 by seeing which button they clicked
       # uses selection
       if self.button_l1_clicked:
           # checks whether the user's input matches the corresponding word in the list
           if get_user_input.lower() == easy_words[self.word_index]:
               # sets the label's text
               self.check_text.config(text="Correct!")
           else:
               self.check_text.config(text="Incorrect!")
               self.mistakes.append(easy_words[self.word_index])
       # checking if the user is playing Level 2 by analyzing which button they clicked
       elif self.button_l2_clicked:
           if get_user_input.lower() == middle_words[self.word_index]:
               self.check_text.config(text="Correct!")
           else:
               self.check_text.config(text="Incorrect!")
               self.mistakes.append(middle_words[self.word_index])
       # checking if the user is playing Level 3
       else:
           if get_user_input.lower() == difficult_words[self.word_index]:
               self.check_text.config(text="Correct!")
           else:
               self.check_text.config(text="Incorrect!")
               self.mistakes.append(difficult_words[self.word_index])
       # uses iteration (see function, remove_duplicates, below)
       self.remove_duplicates()
       self.button_forward.configure(state=tk.NORMAL)

   # ensures that duplicates are not in the list, mistakes
   def remove_duplicates(self):
       for mistake in self.mistakes:
           if self.mistakes.count(mistake) > 1:
               self.mistakes.remove(mistake)

   # allows player to move forward
   def forward(self):
       # increments the index
       self.word_index += 1
       # resets screen to not show output displayed in a previous page
       self.check_text.destroy()
       self.main_page()

   # allows user to navigate between different pages based on input
   def change_page(self, button_num):
       # deletes the widgets from the previous window
       for widget in self.root.winfo_children():
           widget.destroy()
       # checks whether the first page is open
       if self.page_number == 1:
           self.main_page()
           self.page_number = 2
       else:
           self.home_page()
           # resets the list to remove mistakes previously made
           self.mistakes.clear()
           self.page_number = 1
           # resets the index
           self.word_index = 0
       # finds which button is clicked and thus, which level the user is playing
       if button_num == 1:
           self.button_l1_clicked = not self.button_l1_clicked
       elif button_num == 2:
           self.button_l2_clicked = not self.button_l2_clicked
       else:
           self.button_l3_clicked = not self.button_l3_clicked

   # creates user interface for the home screen
   def home_page(self):
       page = tk.Frame(self.root)
       page.grid()
       # placeholder text for proper formatting
       title_text = tk.Label(self.root,
                             text="",
                             font="Times 20",
                             bg='#91EA8B')
       title_text.grid(row=1, column=1, columnspan=3, padx=20, pady=15)
       game_name = tk.Label(self.root,
                            text="SpellNow!",
                            font="Arial 30 bold",
                            bg='#91EA8B')
       game_name.grid(row=2, column=1, columnspan=3, padx=20, pady=15)
       subtext = tk.Label(
           self.root,
           text="Choose a level to begin your spelling adventure!",
           font='Times 16',
           bg='#91EA8B')
       subtext.grid(row=3, column=1, columnspan=3, padx=20, pady=20)
       button_l1 = tk.Button(self.root,
                             text="Level 1",
                             padx=50,
                             pady=30,
                             command=lambda: self.change_page(1),
                             fg='black',
                             bg='#BDEAC8')
       button_l1.grid(row=4, column=1)
       button_l2 = tk.Button(self.root,
                             text="Level 2",
                             padx=40,
                             pady=30,
                             command=lambda: self.change_page(2),
                             fg='black',
                             bg='#BDEAC8')
       button_l2.grid(row=4, column=2)
       button_l3 = tk.Button(self.root,
                             text="Level 3",
                             padx=40,
                             pady=30,
                             command=lambda: self.change_page(3),
                             fg='black',
                             bg='#BDEAC8')
       button_l3.grid(row=4, column=3)
       tk.Label(
           self.root,
           text=
           "You will be spelling 10 different words. Good luck!",
           font='Times 12',
           bg='#91EA8B').grid(row=5, column=1, columnspan=3, padx=20, pady=20)

   # creates user interface for the main playing page
   def main_page(self):
       # deletes widgets from previous outputs
       for widget in self.root.winfo_children():
           widget.destroy()
       inp = tk.StringVar()
       page = tk.Frame(self.root)
       page.pack()
       pronounce_button = tk.Button(self.root,
                                    text="Pronounce it!",
                                    command=lambda: self.pronounce_word(),
                                    bg='#D1EAD7')
       pronounce_button.place(x=240, y=30, height=40, width=140)
       tbox1 = tk.Entry(self.root, textvariable=inp)
       tbox1.place(x=104, y=100, height=60, width=400)
       self.button_check_answer = tk.Button(self.root,
                                            text="Check answer!",
                                            command=lambda: self.check_answer(inp),
                                            bg='#D1EAD7')
       self.button_check_answer.place(x=200, y=180, height=40, width=200)
       self.button_forward = tk.Button(self.root,
                                       text=">>",
                                       bg='#D1EAD7',
                                       command=lambda: self.forward(), state=tk.DISABLED)
       self.button_forward.place(x=440, y=300, height=40, width=90)
       if self.word_index == 10:
           if self.button_check_answer:
               self.button_forward.configure(state=tk.DISABLED)
               self.button_check_answer.configure(state=tk.DISABLED)
               pronounce_button.configure(state=tk.DISABLED)
               button_score = tk.Button(
                   self.root,
                   text='View my score!',
                   command=lambda: self.score_page(),
                   bg='#D1EAD7')
               button_score.place(x=440, y=370, height=40, width=200)

   # user interface for the page that shows the score, mistakes, and other messages.
   def score_page(self):
       for widget in self.root.winfo_children():
           widget.destroy()
       page = tk.Frame(self.root)
       page.pack()
       self.calculate_score()
       # checking whether the user had no mistakes or more than zero errors
       if len(self.mistakes) == 0:
           no_mistakes = tk.Label(self.root,
                                  text="No mistakes!",
                                  font='Times 10',
                                  bg='#91EA8B')
           no_mistakes.place(x=140, y=240, height=40, width=400)
       else:
           for i in self.mistakes:
               output_mistakes = ", ".join(self.mistakes)
           # while the class, WrappingLabel, is from an outside source, the display_mistakes label was created by me
           # I only used the WrappingLabel class to ensure that the words were held within the window boundaries.
           display_mistakes = WrappingLabel(self.root,
                                            text="Your mistakes are: " + output_mistakes,
                                            font='Times 10',
                                            bg='#91EA8B')
           display_mistakes.pack(expand=True, fill=tk.X)
       thanks_message = tk.Label(self.root,
                                 text="Thanks for playing!",
                                 font='Times 10',
                                 bg='#91EA8B',
                                 fg='#1D4762')
       thanks_message.place(x=140, y=340, height=40, width=400)
       return_button = tk.Button(self.root,
                                 text='Return to home!',
                                 command=lambda: self.change_page(2),
                                 bg='#D1EAD7')
       return_button.place(x=240, y=420, height=40, width=200)

   # finding the score and displaying this based on which level was played
   def calculate_score(self):
       if self.button_l1_clicked:
           score = (len(easy_words) - len(self.mistakes))
           display_score = tk.Label(self.root,
                                    text="Your score is: {0}/{1}".format(score, len(easy_words)),
                                    font='Times 10',
                                    bg='#91EA8B')
       elif self.button_l2_clicked:
           score = (len(middle_words) - len(self.mistakes))
           display_score = tk.Label(self.root,
                                    text="Your score is: {0}/{1}".format(score, len(middle_words)),
                                    font='Times 10',
                                    bg='#91EA8B')
       else:
           score = (len(difficult_words) - len(self.mistakes))
           display_score = tk.Label(self.root,
                                    text="Your score is: {0}/{1}".format(score, len(difficult_words)),
                                    font='Times 10',
                                    bg='#91EA8B')
       display_score.place(x=2, y=150, height=40, width=700)

   # ensuring that the first page shown is the home screen and starting the event loop
   def start(self):
       self.home_page()
       # run the tkinter event loop
       self.root.mainloop()


# retrieves the URL for each word's pronunciation and converts it to a .wav file, which gets saved.
def init():
   for word in (*easy_words, *middle_words, *difficult_words):
       url = "https://ssl.gstatic.com/dictionary/static/sounds/oxford/{}--_gb_1.mp3".format(word)
       mp3_file_name = './{}.mp3'.format(word)
       wav_file_name = './{}.wav'.format(word)
       # writing to individual mp3 files to store the audio of the words
       with open(mp3_file_name, 'wb') as f:
           f.write(request.urlopen(url).read())
           sound_wav = AudioSegment.from_file(mp3_file_name, format='mp3')
           # converting mp3 files to wav format
           sound_wav.export(wav_file_name, format='wav')
           f.close()
       # ensures that duplicates of files are not stored when the program is run multiple times
       if os.path.exists(mp3_file_name):
           os.remove(mp3_file_name)


init()
Game().start()

