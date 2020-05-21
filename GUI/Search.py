import tkinter as tk
from PIL import ImageTk
from PIL import Image
from GUI.BookWindow import BookWindow
from MySQL import *
from utils import get_project_root



def bookappWindow(self,bookname):
    bookappWindow= tk.Toplevel(self)
    print(bookname)
    app = BookWindow(bookname,bookappWindow)

class Search():
    # Main window Constructor
    def __init__(self,master):
        self.master= master
        self.master.title("Search")
        self.master.geometry('700x700')
        master.resizable(0, 0)

        #Creates the search entry and button
        SearchEntry = tk.Entry(master,width=20)
        SearchEntry.pack(pady=(50,10))
        SearchButton = tk.Button(master, text='Search', width=10, bg='brown', fg='white',
                                command = lambda : self.Searchapp(self.master,SearchEntry.get(),can,scroll_y))
        SearchButton.pack()

        # Creates the Canvas where we show the search result
        can = tk.Canvas(self.master, height=600, width=330)
        scroll_y = tk.Scrollbar(master, command=can.yview)


    def Searchapp(self,master,searchtext,can,scroll_y):
        can.delete('all')
        frame = tk.Frame(can)
        titleFilenameAuthor = MySQL.SearchBook(self,searchtext)
        width = 100
        height = 100
        pathRoot = get_project_root()
        pathRoot = str(pathRoot)
        No_Image_Cover = pathRoot + "\\projectTest\\BooksCover\\" + "No_Image_Cover.Jpg"
        if len(titleFilenameAuthor) > 0  :
            for filename in titleFilenameAuthor:
                try:
                    img = Image.open(pathRoot + "\\projectTest\\BooksCover\\" +filename[1][:-4]+".Jpg")
                    img = img.resize((width, height), Image.ANTIALIAS)
                    photoImg = ImageTk.PhotoImage(img)
                    panel = tk.Button(frame,image=photoImg)
                    panel.config(command=lambda bookname= filename[0],: bookappWindow(self.master,bookname) )
                    panel.image =photoImg
                    title = tk.Label(frame, text=filename[0], font=("bold", 10))
                    panel.pack()
                    title.pack()
                except:
                    img = Image.open(No_Image_Cover)
                    img = img.resize((width, height), Image.ANTIALIAS)
                    photoImg = ImageTk.PhotoImage(img)
                    panel = tk.Button(frame,image=photoImg)
                    panel.config(command=lambda bookname=filename[0],: bookappWindow(self.master, bookname))
                    panel.image = photoImg
                    panel.pack()
                    title = tk.Label(frame, text=filename[0], font=("bold", 10))
                    title.pack()

            can.create_window(0, 0, anchor='nw', window=frame)
            can.update_idletasks()
            can.configure(scrollregion=can.bbox('all'), yscrollcommand=scroll_y.set)
            scroll_y.pack(fill='y', side='right')
            can.pack(pady=(30,10))
        else:
            tk.messagebox.showinfo("Sorry", "We didn't find what you wanted!")
