#python chatwindow program
#Import the library (This whole thing works on tkinker)
from tkinter import *
from tkinter import font
from tkinter import ttk
from datetime import datetime
#from chat import get_response, bot_name 
#holdover from "insert name window", 
user_name = "You"

BG = "#ffefd5"
BGtext = "#ffffff"
FGtext = "#000000"


class chat_GUI:


    def __init__(self):
        #create chat window
        self.Window = Tk()
        self.Setup()

    def run(self):
        self.Window.mainloop()

    def Setup(self):
        print ("Window setup")

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
                              text = "Libot interface V0.4",
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
        self.chat_insert(message, user_name)

    #insert from messenger into chatscreen
    def chat_insert(self, message, sender):
        #if messenger is empty dont trigger
        if not message:
            return

        #clear messenger when message is sent
        self.messenger.delete(0, END)
        #dump message from user on the end of the chatlog
        usermessage = f"{sender}: {message} \n"
        self.chatscreen.configure(state=NORMAL)
        self.chatscreen.insert(END, usermessage)
        self.chatscreen.configure(state=DISABLED)

        #bot response debug command
        botmessage = "Testing bot: Response!\n"

        #chatbot response
        #botmessage = f"{bot_name}: {get_response{message}} \n"
        self.chatscreen.configure(state=NORMAL)
        self.chatscreen.insert(END, botmessage)
        self.chatscreen.configure(state=DISABLED)
        self.writelog(usermessage, botmessage)

        #autoscroll to the end when sending
        self.chatscreen.see(END)

    #write a chatlog (NOTE: intensive, will be cleaned up to provide greater efficency)
    def writelog(self, usermessage, botmessage):
        savefile = open("logged conversation.txt", "a")
        timestamp = datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        contents = timestamp + "\n" + usermessage + "\n" + timestamp + "\n" + botmessage + "\n"
        savefile.write(contents)
        savefile.close()

if __name__ == "__main__":
    app = chat_GUI()
    app.run()
