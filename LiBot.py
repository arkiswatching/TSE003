#General imports
import os
import sys
import re
import string
import threading
#Imports for GUI
import tkinter
from tkinter import *
from datetime import datetime
#Imports for the dataframe/knowledgebase
import pandas as pd
import numpy as np
#Imports for speech recognition
import speech_recognition as speech
import pipwin
import pyaudio
#Imports for word processing
import nltk
nltk.download('popular', quiet = True) 
from nltk.stem import wordnet
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from collections import defaultdict
#Imports for similarity
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

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
                              text = "LiBot",
                               font = "sans-serif 14 bold",
                               pady = 5)
        self.Title.place(relwidth = 1)

        #voice chat button
        voicebutton = Button(self.Title,
                                text = "🎤",
                                font = "sans-serif 11", 
                                bg = "#002654",
                                fg = "white")
        voicebutton.bind('<ButtonPress-1>', self.voicerun)

        voicebutton.place(relx = 0.95,
                             rely = 0.20,
                             relheight = 0.70, 
                             relwidth = 0.05)
        
        #chatscreen interface (shows chat to date)
        self.chatscreen = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = BGtext,
                             fg = FGtext,
                             font = "sans-serif 12",
                             wrap = WORD,
                             padx = 5,
                             pady = 5,
                             cursor = "arrow")

        self.chatscreen.place(relheight = 0.805,
                            relwidth = 0.95, 
                            rely = 0.08)
        
        #message colouration tags
        self.chatscreen.tag_config('bot', background = BGbot)
        self.chatscreen.tag_config('error', background = BGerror)

        #initial chat welcome message
        self.chat_insert_response(welcome)
        #self.chatscreen.configure(cursor="arrow")
        
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
                              font = "sans-serif 12")

        #place the enter message widget in the main window
        self.messenger.place(relwidth = 0.70,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
        
        #messenger interface scrollbar (in case of extended entry)
        messengerscrollbar = Scrollbar(self.messengerplace)
        # place the scroll bar on window so doesn't cover message box at all
        messengerscrollbar.place(relheight = 0.06,
                                  relx = 0.72,
                                  rely = 0.008
                                  )
        #command so it scrolls the text (y-axis)
        messengerscrollbar.config(command = self.messenger.yview)

        #auto focus on the entry message box when the window is active
        self.messenger.focus()
        #enter command functionality
        self.messenger.bind("<Return>", self.entermsg)
        #when escaped out, the program saves to the log and exits.
        self.messenger.bind("<Escape>", self.quit)
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
        message = message.strip("\n")
        #if messenger is empty dont trigger
        if not message:
            return 'break'
        else:
            self.chat_insert_message(message)
            response = get_response(message, df)
            self.chat_insert_response(response)
            return 'break'

    def chat_insert(self, text):
        self.chatscreen.configure(state=NORMAL)
        self.chatscreen.insert(END, text)
        self.chatscreen.configure(state=DISABLED)
        savefile.write(text)
        
    #insert from messenger into chatscreen
    def chat_insert_message(self, message):
        #clear messenger when message is sent (values to take row 1, character 0 to end)
        self.messenger.delete(1.0, END)
        #dump message from user on the end of the chatlog
        usermessage = f"{user_name}: {message}\n"
        self.chat_insert(usermessage)
        self.chat_insert("\n")

    def chat_insert_response(self, response):
        #chatbot response
        botmessage = f"{bot_name}: {response}\n"
        self.chatscreen.configure(state=NORMAL)
        #if statement to change colour of the message bg if the response is an error (NOTE: ad "notfound" if "response not found" is going to change colour).
        if (response == requesterror or response == unknownvalueerror or response == unboundlocalerror):
            self.chatscreen.insert(END, botmessage, 'error')
        else:
            self.chatscreen.insert(END, botmessage, 'bot')
        self.chatscreen.configure(state=DISABLED)
        #write the user input and reply to the savefile log
        savefile.write(botmessage)
        #autoscroll to the end when sending
        self.chat_insert("\n")
        self.chatscreen.see(END)

    #function to run the voice input on a thread.
    def voicerun(self, event):
        self.chat_insert_response(listening)
        voice_thread = threading.Thread(target = self.voiceinput)
        voice_thread.start()

    #voice chat function
    def voiceinput(self):
        robot = speech.Recognizer()
        microphone = speech.Microphone()
        with microphone as source:
            audio = robot.listen(source) #recieves voice input from microphone
        try:
            self.messenger.insert(END, robot.recognize_google(audio))
            self.entermsg(None)
        #error handling
        except speech.UnknownValueError:
            self.chat_insert_response(unknownvalueerror)
        except speech.RequestError:
            self.chat_insert_response(requesterror)
        except speech.UnboundLocalError:
            self.chat_insert_response(unboundlocalerror)

    #save the chatlog and close if escape is pressed (NOTE: only works when escaped out)
    def quit(self, event):
        savefile.close()
        self.Window.destroy()

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

def get_response(message, df):
    norm_message = txt_normaliser(message)
    tfidf = TfidfVectorizer(stop_words = stopwords.words('english')) # initialises vectorizor
    df_tfidf = tfidf.fit_transform(df['Normalised Context']).toarray() # vectorizing context into array
    input_tfidf = tfidf.transform([norm_message]).toarray() # vectorizing input into array
    cos_sim = 1 - pairwise_distances(df_tfidf,input_tfidf,metric = 'cosine') # performs cosine similarity between vectoried data and input
    index = cos_sim.argmax() # finds largest similarity values index
    if cos_sim[index] < 0.6:
        get_response = notfound
    else:
        get_response = df['Response'].loc[index]
    return get_response

#user and bot name
user_name = "User"
bot_name = "LiBot"

#message strings (focused to make tweaking messages easier)
welcome = "Hello! I'm " + bot_name + ", a chatbot created to help you with any questions you may have regarding the University of Lincoln's library. Press the 'esc' key if you wish to exit."
listening = "What would you like to say? Please speak clearly so I can understand you."
unknownvalueerror = "Sorry, I didn't hear what you said. Please try again or type in the box below."
requesterror = "Sorry, I cannot access a microphone at this time. Please try again or type in the box below."
unboundlocalerror = "Sorry, the voice functionality is experiencing difficulty right now. Please try again or type in the box below."
notfound = "Sorry, I didn't understand that."

#colouration settings, makes it easier to do sweeping changes to the UI scheme
BG = "#002654"
BGtext = "#ffffff"
FGtext = "#000000"
BGbot = "#cce0ff"
BGerror = "#ffff99"

#save file data
timestamp = datetime.now()
timestamp = timestamp.strftime("%Y-%m-%d %H-%M-%S")

#File location variable.
filepath = 'chatlog'
if os.path.exists(filepath) == False:
    os.mkdir(filepath)
savefile = open(filepath + '\\' + str(timestamp) + ".txt", "a")

#Get file path
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

#Create a dataframe/knowledge base
df = pd.read_excel(application_path + "\\Library_Knowledge_Base.xlsx", usecols = ['Context', 'Response']) # reads excel file
df.ffill(axis = 0, inplace = True) # fills 'NaN' cells
df['Normalised Context'] = df['Context'].apply(txt_normaliser) # creates normalised column using a function

#Runs the application
if __name__ == "__main__":
    app = chat_GUI()
    app.run()
