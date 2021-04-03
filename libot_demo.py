# trys to import packages, on error they are downloaded then imported
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
import os
import subprocess
import sys
import re
nltk.download('popular', quiet=True)
from sklearn.feature_extraction.text import TfidfVectorizer # to perform tfidf
from sklearn.metrics import pairwise_distances # to perform cosine similarity
from nltk.stem import wordnet # to perform lemmitization
from nltk import pos_tag # for parts of speech
from nltk import word_tokenize # to create tokens
from nltk.corpus import stopwords # for stop words (needs integrating)


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
        self.Window.title("Chat program")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = BG)
        self.Title = Label(self.Window,
                             bg = BG, 
                              fg = FGtext,
                              text = "LiBot interface V0.4",
                               font = "Helvetica 13 bold",
                               pady = 5)
        self.Title.place(relwidth = 1)

        #chatscreen interface (shows chat to date)
        self.chatscreen = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = BGtext,
                             fg = FGtext,
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
        self.chatscreen.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
        self.chatscreen.configure(cursor="arrow", state=DISABLED)
        self.chatscreen.configure(state=NORMAL)
        welcome = "LiBot: Hello! I'm LiBot, a chatbot created to help you with any questions you may have regarding the University of Lincoln's library. Press the 'esc' key if you wish to exit.\n\n"
        self.chatscreen.insert(END, welcome)
        savefile.write(welcome)
        self.chatscreen.configure(state=DISABLED)
        
        #chatscreen interface scrollbar (self evidant what its for)
        scrollbar = Scrollbar(self.chatscreen)
        # place the scroll bar on chatscreen (NOT WINDOW)
        scrollbar.place(relheight = 1,
                        relx = 0.974)
        #command so it scrolls the text (y-axis)
        scrollbar.config(command = self.chatscreen.yview)

        #cosmetic labelling/placement of messenger
        self.messengerplace = Label(self.Window,
                                 bg = BG,
                                 height = 80)
        
        self.messengerplace.place(relwidth = 1,
                               rely = 0.825)

        #widget for user to enter text
        self.messenger = Entry(self.messengerplace,
                              bg = BGtext,
                              fg = FGtext,
                              font = "Helvetica 13")

        #place the enter message widget in the main window
        self.messenger.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
        
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
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = BG,
                                command = lambda: self.entermsg(None))

        sendbutton.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)

    #function to send if enter is pressed
    def entermsg(self, event):
        message=self.messenger.get()
        response = get_response(message)
        self.chat_insert(message, response)

    #insert from messenger into chatscreen
    def chat_insert(self, message, response):
        #if messenger is empty dont trigger
        if not message:
            return

        #clear messenger when message is sent
        self.messenger.delete(0, END)
        #dump message from user on the end of the chatlog
        usermessage = f"{user_name}: {message} \n\n"
        self.chatscreen.configure(state=NORMAL)
        self.chatscreen.insert(END, usermessage)
        self.chatscreen.configure(state=DISABLED)

        #bot response debug command
        #botmessage = "Testing bot: Response!\n"

        #chatbot response
        botmessage = f"{bot_name}: {response} \n\n"
        self.chatscreen.configure(state=NORMAL)
        self.chatscreen.insert(END, botmessage)
        self.chatscreen.configure(state=DISABLED)
        #write the user input and reply to the savefile log
        savefile.write(usermessage+botmessage)

        #autoscroll to the end when sending
        self.chatscreen.see(END)

    #save the chatlog and close if escape is pressed (NOTE: only works when escaped out)
    def quit(self, event):
        savefile.close()
        self.Window.destroy()


def text_normalisation(text):
        text=str(text).lower() # text to lower case
        spl_char_text=re.sub(r'[^ a-z]','',text) # removing special characters
        tokens=nltk.word_tokenize(spl_char_text) # word tokenizing
        lema=wordnet.WordNetLemmatizer() # intializing lemmatization
        tags_list=pos_tag(tokens,tagset=None) # parts of speech
        lema_words=[] # empty list
        for token,pos_token in tags_list:
            if pos_token.startswith('V'): #verbs
                pos_val= 'v'
            elif pos_token.startswith('J'): #Adjective
                pos_val='a'
            elif pos_token.startswith('R'): #adverb
                pos_val= 'r'
            else:
                pos_val= 'n' # noun
            lema_token=lema.lemmatize(token,pos_val) # performing lemmatization
            lema_words.append(lema_token) # appending the lematized token into lists
        return " ".join(lema_words) # returns the lematized token into sentences

def get_response(message):
        norm_message = text_normalisation(message)
        tfidf = TfidfVectorizer() # initialises vectorizor
        df_tfidf = tfidf.fit_transform(df['Normalised Context']).toarray() # vectorizing context into array
        input_tfidf = tfidf.transform([norm_message]).toarray() # vectorizing input into array
        cos_sim = 1 - pairwise_distances(df_tfidf,input_tfidf,metric = 'cosine') # performs cosine similarity between vectoried data and input
        index = cos_sim.argmax() # finds largest similarity values index
        if cos_sim[index] < 0.4:
            get_response = "Sorry, I didn't understand that."
        else:
            get_response = df['Response'].loc[index]
        return get_response

#user and bot name
user_name = "User"
bot_name = "LiBot"

#colouration settings, makes it easier to do sweeping changes to the UI scheme
BG = "#ffefd5"
BGtext = "#ffffff"
FGtext = "#000000"

#save file data
timestamp = datetime.now()
timestamp = timestamp.strftime("%Y-%m-%d %H-%M-%S")
filename = str(timestamp) + ".txt"
savefile = open(filename, "a+")

file_dir = os.path.dirname(os.path.abspath(__file__)) # assigns file directory to a variable
df = pd.read_excel(file_dir + "\Library_Knowledge_Base.xlsx", usecols = ['Context', 'Response']) # reads excel file
df.ffill(axis = 0, inplace = True) # fills 'NaN' cells
df['Normalised Context'] = df['Context'].apply(text_normalisation) # creates normalised column using a function

if __name__ == "__main__":
    app = chat_GUI()
    app.run()
