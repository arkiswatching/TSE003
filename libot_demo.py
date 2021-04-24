# trys to import packages, on error they are downloaded then imported
import os
import subprocess
import sys
import re
import string
import threading
#attempt at fixing the cmd "no module named BLANK" error
try:
    import wheel
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'wheel'])
finally:
    import wheel
try:
    import pandas as pd
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
finally:
    import pandas as pd
    import numpy as np
try:
    import nltk
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'nltk'])
finally:
    import nltk
try:
    import sklearn
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'sklearn'])
finally:
    import sklearn
try:
    import openpyxl
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'openpyxl'])
finally:
    import openpyxl
try:
    from spellchecker import SpellChecker
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyspellchecker'])
finally:
    from spellchecker import SpellChecker
########################speech recognition imports##########################################
try:
    import speech_recognition as speech
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'SpeechRecognition'])
finally:
    import speech_recognition as speech# import speech
try:
    import pipwin
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pipwin'])
finally:
    import pipwin
try:
    import pyaudio
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pipwin", "install", 'pyaudio'])
finally:
    import pyaudio #import mic capability
#########################speech recognition import end###################################
nltk.download('popular', quiet = True) 
from sklearn.feature_extraction.text import TfidfVectorizer # to perform tfidf
from sklearn.metrics import pairwise_distances # to perform cosine similarity
from nltk.stem import wordnet # to perform lemmitization
from nltk import pos_tag # for parts of speech
from nltk import word_tokenize # to create tokens
from nltk.corpus import stopwords # for stop words (needs integrating)
from nltk.corpus import wordnet as wn
from collections import defaultdict


#python chatwindow program
#Import the library (This whole thing works on tkinker, datetiime, and of course the libot program)
try:
    import tkinter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'tkinter'])
finally:
    import tkinter
from tkinter import *
from tkinter import font
from tkinter import ttk
from datetime import datetime
#from libot.py import get_response, bot_name 

class chat_GUI:

    def __init__(self):
        #create chat window
        self.Window = Tk()
        self.Setup()

    def run(self):
        self.Window.mainloop()

    def Setup(self):

        #building the actual core program window
        self.Window.title("LiBot - University of Lincoln Library Chatbot")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 500,
                              height = 550,
                              bg = "#345c97")
        self.Title = Label(self.Window,
                             bg = "#002654", 
                              fg = "white",
                              text = "LiBot interface V0.4",
                               font = "sans-serif 14 bold",
                               pady = 5)
        self.Title.place(relwidth = 1)
        
        ###################button start#################################
        voicebutton = Button(self.Title,
                                text = "🎤",
                                font = "sans-serif 11", 
                                #width = 20,
                                #height = 20,
                                bg = "#002654",
                                fg = "white")

        #still getting voice function to work, but the button, its placement and method of acknowledgment has been fixed to bind to the function when integrated properly.
        #voicebutton.bind('<ButtonPress-1>', self.voiceinput)
        voicebutton.bind('<ButtonPress-1>', self.voicemessage)

        voicebutton.place(relx = 0.95,
                             rely = 0.20,
                             relheight = 0.70, 
                             relwidth = 0.05)
        ###################button end#################################
        
        #chatscreen interface (shows chat to date)
        self.chatscreen = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = BGtext,
                             fg = FGtext,
                             font = "sans-serif 12",
                             #wrapping perameter
                             wrap = WORD,
                             padx = 5,
                             pady = 5)
        self.chatscreen.place(relheight = 0.805,
                            relwidth = 0.95, 
                            rely = 0.08)
        self.chatscreen.configure(cursor="arrow", state=DISABLED)
        self.chatscreen.configure(state=NORMAL)
        welcome = "LiBot: Hello! I'm LiBot, a chatbot created to help you with any questions you may have regarding the University of Lincoln's library. Press the 'esc' key if you wish to exit.\n\n"
        self.chatscreen.insert(END, welcome)
        savefile.write(welcome)
        self.chatscreen.configure(state=DISABLED)
        
        #chatscreen interface scrollbar (self evidant what its for)
        scrollbar = Scrollbar(self.Window)
        # place the scroll bar on window so doesn't cover chatscreen
        scrollbar.place(relheight = 0.805,
                        rely = 0.08,
                        relx = 0.958)
        #command so it scrolls the text (y-axis)
        scrollbar.config(command = self.chatscreen.yview)

        #cosmetic labelling/placement of messenger
        self.messengerplace = Label(self.Window,
                                 bg = "#002654",
                                 height = 50)
        
        self.messengerplace.place(relwidth = 1,
                               rely = 0.885)

        #widget for user to enter text
        #text used over entry to allow for wrapping
        self.messenger = Text(self.messengerplace,
                              bg = BGtext,
                              fg = FGtext,
                              wrap = WORD,
                              #padx = 5,#, 10),
                              #wraplength = 500,
                              font = "sans-serif 12")

        #place the enter message widget in the main window
        #self.messenger.place(relwidth = 0.74,
        self.messenger.place(relwidth = 0.70,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
        
        #messenger interface scrollbar (self evidant what its for)
        messengerscrollbar = Scrollbar(self.messengerplace)
        # place the scroll bar on window so doesn't cover chatscreen
        messengerscrollbar.place(relheight = 0.06,
                                  relx = 0.72,
                                  rely = 0.008
                                  )
                                  #relx = 0.958)
        #command so it scrolls the text (y-axis)
        messengerscrollbar.config(command = self.messenger.yview)

        #auto focus on the entry message box when the window is active
        self.messenger.focus()
        #enter command functionality
        self.messenger.bind("<Return>", self.entermsg)
        #when escaped out, the program saves to the log and exits.
        self.messenger.bind("<Escape>", self.quit)
        #self.protocol(WM_DELETE_WINDOW, self.quit)
        #sendbutton coding 
        sendbutton = Button(self.messengerplace,
                                text = "Send",
                                font = "sans-serif 11 bold", 
                                width = 20,
                                bg = "#002654",
                                fg = "white",
                                command = lambda: self.entermsg(None))

        sendbutton.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)

    #function to send if enter is pressed
    def entermsg(self, event):
        #values to take row 1, character 0 to end
        message = self.messenger.get(1.0, END)
        self.chat_insert_message(message)
        message = spell_check(message)
        response = get_response(message)
        self.chat_insert_response(response)

    #insert from messenger into chatscreen
    def chat_insert_message(self, message):
        #if messenger is empty dont trigger
        if not message:
            return
        else:
            #clear messenger when message is sent
            #values to take row 1, character 0 to end
            self.messenger.delete(1.0, END)
            #dump message from user on the end of the chatlog
            usermessage = f"{user_name}: {message} \n\n"
            self.chatscreen.configure(state=NORMAL)
            self.chatscreen.insert(END, usermessage)
            self.chatscreen.configure(state=DISABLED)
            savefile.write(usermessage)

    def chat_insert_response(self, response):
        #bot response debug command
        #botmessage = "Testing bot: Response!\n"

        #chatbot response
        botmessage = f"{bot_name}: {response} \n\n"
        self.chatscreen.configure(state=NORMAL)
        self.chatscreen.insert(END, botmessage)
        self.chatscreen.configure(state=DISABLED)
        #write the user input and reply to the savefile log
        savefile.write(botmessage)

        #autoscroll to the end when sending
        self.chatscreen.see(END)
        
        ##########################voicemessage#####################################################
    def voicemessage (self, event):
        self.chatscreen.configure(state=NORMAL)
        self.chatscreen.insert(END, bot_name + ": What would you like to say? Please speak clearly so I can understand you.\n\n")
        self.chatscreen.configure(state=DISABLED)
        self.chatscreen.see(END)
        self.voiceinput(event)#, robot, microphone)
        ############################voicemessage end###############################################

    ########################voice addition v4######################################################
    def voiceinput(self, event):
        def voicemessage(self, event):
            #debug command to test button, to be removed when function the function is finished
            print ("acknowledged.") ###################################################
            robot = speech.Recognizer()
            microphone = speech.Microphone()
            with microphone as source:
                audio = robot.listen(source) #recieves voice input from microphone
            try:
                self.messenger.insert(END, robot.recognize_google(audio))
                self.entermsg(None)
            except speech.UnknownValueError:
                self.chatscreen.configure(state=NORMAL)
                self.chatscreen.insert(END, bot_name + ": Sorry, I didn't hear what you said. Please try again or type in the box below.\n\n")
                self.chatscreen.configure(state=DISABLED)
                self.chatscreen.see(END)
                print("Unknown voice input.")
            except speech.RequestError:
                self.chatscreen.configure(state=NORMAL)
                self.chatscreen.insert(END, bot_name + ": Sorry, I cannot access a microphone at this time. Please try again or type in the box below.\n\n")
                self.chatscreen.configure(state=DISABLED)
                self.chatscreen.see(END)
                print("Something went wrong, error {0}".format(error))
            except speech.UnboundLocalError:
                self.chatscreen.configure(state=NORMAL)
                self.chatscreen.insert(END, bot_name + ": Sorry, the voice functionality is experiencing difficulty right now. Please try again or type in the box below.\n\n")
                self.chatscreen.configure(state=DISABLED)
                self.chatscreen.see(END)
                print("Something went wrong, error {0}".format(error)) 
        a_thread = threading.Thread(target = voicemessage(self, event))
        a_thread.start()
    ########################voice addition v4 end######################################################
        
    #save the chatlog and close if escape is pressed (NOTE: only works when escaped out)
    def quit(self, event):
        savefile.close()
        self.Window.destroy()

def spell_check(text):
    text = text.split(" ")
    i = 0
    for word in text:
        text[i] = SpellChecker().correction(word)
        i = i + 1
    return " ".join(text)

def txt_normaliser(text):
    text = str(text).lower() # text to lower case
    spl_char_text=re.sub(r'[^ a-z]','',text) #removing special characters
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    wordTokenizer = nltk.word_tokenize(text.translate(remove_punct_dict)) #tokenizer
    #pos tagging and lemmatization
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    ltizer = wordnet.WordNetLemmatizer()
    ltizer_words= []
    rmv = [i for i in wordTokenizer if i]
    for token, tag in nltk.pos_tag(rmv):
        lemma = ltizer.lemmatize(token, tag_map[tag[0]])
        ltizer_words.append(lemma)
    return " ".join(ltizer_words)

def get_response(message):
    norm_message = txt_normaliser(message)
    tfidf = TfidfVectorizer(stop_words = stopwords.words('english')) # initialises vectorizor
    df_tfidf = tfidf.fit_transform(df['Normalised Context']).toarray() # vectorizing context into array
    input_tfidf = tfidf.transform([norm_message]).toarray() # vectorizing input into array
    cos_sim = 1 - pairwise_distances(df_tfidf,input_tfidf,metric = 'cosine') # performs cosine similarity between vectoried data and input
    index = cos_sim.argmax() # finds largest similarity values index
    if cos_sim[index] < 0.6:
        get_response = "Sorry, I didn't understand that."
    else:
        get_response = df['Response'].loc[index]
    return get_response

#user and bot name
user_name = "User"
bot_name = "LiBot"

#colouration settings, makes it easier to do sweeping changes to the UI scheme
BG = "#002654"
BGtext = "#ffffff"
FGtext = "#000000"

#save file data
timestamp = datetime.now()
timestamp = timestamp.strftime("%Y-%m-%d %H-%M-%S")
savefile = open(str(timestamp) + ".txt", "a")

file_dir = os.path.dirname(os.path.abspath(__file__)) # assigns file directory to a variable
df = pd.read_excel(file_dir + "\Library_Knowledge_Base.xlsx", usecols = ['Context', 'Response']) # reads excel file
df.ffill(axis = 0, inplace = True) # fills 'NaN' cells
df['Normalised Context'] = df['Context'].apply(txt_normaliser) # creates normalised column using a function

if __name__ == "__main__":
    app = chat_GUI()
    app.run()
