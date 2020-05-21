import tkinter as tk
from MySQL import *
from utils import get_project_root





class BookWindow():
    # Main window Constructor
    def __init__(self, bookname , master):
        print(bookname)
        self.master=master
        self.master.title("BookWindow")
        self.master.geometry('1200x700')
        master.resizable(0, 0)
        filename = MySQL.getFileName(self,bookname)
        root_dir = get_project_root()
        root_dir = str(root_dir)
        root_dir = root_dir + "\\" + "projectTest\\"
        print(filename)
        f = open(root_dir+"read_book\\"+filename)
        lines = f.readlines()
        for line in lines:
            line = line.rstrip("\n")
        Booktext = tk.Text(self.master, height=100, width=110)
        scroll = tk.Scrollbar(self.master, command=Booktext.yview)

        Booktext.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        Booktext.tag_configure('big', font=('Verdana', 20, 'bold'))
        Booktext.tag_configure('color',
                            foreground='#476042',
                            font=('Tempus Sans ITC', 12, 'bold'))
        book=''
        for line in lines:
            book=book+(line.rstrip("\n"))+"\n"
        quote =str(book)
        Booktext.insert(tk.END, quote, 'color')
        Booktext.configure(yscrollcommand=scroll.set)
        Booktext.configure(state='disabled')
        Booktext.pack()
        scroll.pack(fill='y', side='right')




