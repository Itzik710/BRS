import os
import tkinter as tk
from tkinter import Label, Entry, Button, Toplevel,messagebox
from GUI.Main import Main
from MySQL import *

# Login Window
class login():
    #Login window Constructor
    def __init__(self, master):
        # Set up Log-in screen
        self.master = master
        master.geometry('500x500')
        master.title("Log-In")
        master.resizable(0, 0)

        # Create Book NetBooks Label
        netbooksLabel = Label(master, text="NetBook", width=20, font=("bold", 20))
        netbooksLabel.place(x=90, y=53)

        # Create username Label and Entry
        idLabel = Label(master, text="Id", width=20, font=("bold", 10))
        idLabel.place(x=80, y=130)
        idEntry = Entry(master)
        idEntry.place(x=210, y=130)

        # Create password Label and Entry
        passwordLabel_2 = Label(master, text="Password", width=20, font=("bold", 10))
        passwordLabel_2.place(x=80, y=180)
        passwordEntry = Entry(master)
        passwordEntry.place(x=210, y=180)

        # Create a log-in button
        # When you click a button,a function mainappWindow is activated which receives the user ID and password
        logInButton = Button(master, text='Submit', width=20, bg='brown', fg='white',
                             command = lambda : self.mainappWindow(idEntry.get(),passwordEntry.get(),self.master,passwordEntry,idEntry))\
                             .place(x=180, y=350)





    # A function that opens the main window
    # The word empty indicates that one of the fields is empty
    # The word True indicates that login was successfuly
    # and else  is a situation where one of the fields is incorrect
    def mainappWindow(self,id,password,master,passwordEntry,idEntry):
        imesg = MySQL.login(self,id,password)
        # User did not entered input - (id, password, both)
        if (imesg == "empty"):
            tk.messagebox.showinfo("Error", "One of the fields is empty Please fill in all fields as required ")
        # User entered correct input - (id, password)
        elif (imesg == True):
            # main = Toplevel(self.master)
            app = Main(id,self.master)
            #master.quit()
        # User entered wrong input - (id, password, both)
        else:
            tk.messagebox.showinfo("Error", 'Incorrect Input, Please Try Again ')
            passwordEntry.delete(0, 'end')
            idEntry.delete(0, 'end')


# Program main function
def main():
    root = tk.Tk()
    login(root)
    root.mainloop()
if __name__ == '__main__':
        main()


