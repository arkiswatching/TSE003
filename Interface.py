#Description: This is a chat bot GUI

#Import the library
from tkinter import *

def savelog():
    savefile = open("logged conversation.txt", "a")
    from datetime import datetime
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    contents = "\n" + timestamp + "\nAll text goes here. Replace with actual contents in later build.\n"
    savefile.write(contents)
    savefile.close()

root = Tk()
root.title("Chat Bot")
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)
main_menu = Menu(root)

# Create the submenu 
file_menu = Menu(root)

# Add commands to submenu
file_menu.add_command(label="New..")#, command=root)
file_menu.add_command(label="Save As..", command=savelog())
file_menu.add_command(label="Exit", command=root.destroy)
main_menu.add_cascade(label="File", menu=file_menu)
#Add the rest of the menu options to the main menu, have been removed but may be useful for archive if needed.
#main_menu.add_command(label="Edit")
#main_menu.add_command(label="Quit")
root.config(menu=main_menu)

chatWindow = Text(root, bd=1, bg="black",  width="50", height="8", font=("Arial", 23), foreground="#00ffff")
chatWindow.place(x=6,y=6, height=385, width=370)

messageWindow = Text(root, bd=0, bg="black",width="30", height="4", font=("Arial", 23), foreground="#00ffff")
messageWindow.place(x=128, y=400, height=88, width=260)

scrollbar = Scrollbar(root, command=chatWindow.yview, cursor="star")
scrollbar.place(x=375,y=5, height=385)

Button= Button(root, text="Send", width="12", height=5, command = "hello", bd=0, bg="#0080ff", activebackground="#00bfff",foreground='#ffffff',font=("Arial", 12))
Button.place(x=6, y=400, height=88)
#Button(command(text="TEST"))

root.mainloop()
