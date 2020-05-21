import os
from tkinter import *
from GUI.Search import *
from MySQL import *
from SVR import  getUserRecommendedList
from sklearn.utils import shuffle
from utils import get_project_root




def SearchappWindow(self):
    SearchappWindow = Toplevel(self)
    app = Search(SearchappWindow)

def bookappWindow(self,bookname):
    bookappWindow=Toplevel(self)
    app = BookWindow(bookname,bookappWindow)


def ratingappWindow(self, bookname,id,rating,w):
    try:
        if int(rating) < 6 and int(rating)>-1:
            filename = MySQL.getFileName(self,bookname)
            IdUserInBook = MySQL.GetTheLastIdInBookInUser(self)
            result= MySQL.InsertNewBookToUserReadingHistory(self, filename,id,rating,IdUserInBook)
            if result== TRUE:
                tk.messagebox.showinfo("Success", "Rated successfully")
                w.delete(0, 'end')
        else:
            tk.messagebox.showinfo("Error", 'Invalid Input')
            w.delete(0, 'end')
    except:
        tk.messagebox.showinfo("Error", 'Invalid Input')
        w.delete(0, 'end')


class Main():
    title = ""
    # Main window Constructor
    def __init__(self, id , master):

        self.master = master
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.title("Main")
        self.master.geometry('1200x700')
        master.resizable(0, 0)

        # creat menu bar whit personal data , search and exit tag
        root_menu = Menu(master)
        master.config(menu=root_menu)
        file_menu = Menu(root_menu)  # it intializes a new su menu in the root menu
        root_menu.add_cascade(label="MainBar", menu=file_menu)  # it creates the name of the sub menu
        file_menu.add_command(label="Search", command=lambda: SearchappWindow(self.master))
        file_menu.add_separator()  # it adds a line after the 'Open files' option
        file_menu.add_command(label="Exit", command=master.quit)

        # books cover images
        pathRoot = get_project_root()
        pathRoot = str(pathRoot)
        No_Image_Cover = pathRoot + "\\projectTest\\BooksCover\\" + "No_Image_Cover.Jpg"

        #creat list of recomended book for the user
        # get all user's book recommendations from SVR class - [filename, rating]
        userRatingBooks = getUserRecommendedList("", id)
        userRatingBooks=shuffle(userRatingBooks)
        #Introduce one of the books first
        self.BookDetails(userRatingBooks[0], pathRoot,"predict",No_Image_Cover)

        # Create a Read button
        ReadnowButton = Button(self.master, text='Read Now', width=30, font=("bold", 8), bg='brown', fg='white',
                               command=lambda : bookappWindow(self.master.master, self.title) ).place(x=50, y=150)

        # Create a Rating Spinbox
        w = Spinbox(self.master, from_=0, to=5)
        w.place(x=400, y=150)
        # Create a Rating button
        RatingButton = Button(self.master, text='Rating', width=15, font=("bold", 8), bg='blue', fg='white',
                           command=lambda : ratingappWindow(self,self.title,id,w.get(),w) ).place(x=250, y=150)


        #Create Rating frame whit label and button
        RatingLabel = Label(self.master, text='Rating:', font=("bold", 10))
        RatingLabel.place(x=50, y=200)
        self.setBooksOnScreen(pathRoot, userRatingBooks, 220,"predict",No_Image_Cover)

        # Create history frame whit label and button
        historyLabel = Label(self.master, text='History:', font=("bold", 10))
        historyLabel.place(x=50, y=350)
        historylist = MySQL.getbook(self,id)
        self.setBooksOnScreen(pathRoot, historylist, 370,"History",No_Image_Cover)

        # Create New frame whit label and button
        NewLabel = Label(self.master, text="New Books:", font=("bold", 10))
        NewLabel.place(x=50, y=500)
        Newlist = MySQL.getAllBooks(self)
        Newlist=shuffle(Newlist)
        self.setBooksOnScreen(pathRoot, Newlist, 520,"New",No_Image_Cover)
    # show the Details of a book
    def BookDetails(self, bookname, pathRoot, type,No_Image_Cover):
        filename = bookname[0]
        TitleAuthor = MySQL.getAuthor(self, filename )
        self.title = TitleAuthor[0]
        # Create Book NetBooks Label
        booknameLabel = Label(self.master, text=self.title, width=70, font=("bold", 10)).place(x=60, y=25)
        AuthornameLabel = Label(self.master, text="Author Name:", width=10, font=("bold", 8)).place(x=50, y=50)
        nameLabel = Label(self.master, text=TitleAuthor[1], width=20, font=("bold", 8)).place(x=140, y=50)
        #if it prdict list we show the rating
        if type == "predict":
            predictLabel = Label(self.master, text="Rating:", width=10, font=("bold", 8)).place(x=35, y=70)
            predictnumLabel = Label(self.master, text=str(int(bookname[1])) + '%', width=10, font=("bold", 8)).place(
                x=100, y=70)
        else:
            predictLabel = Label(self.master, text="         ", width=10, font=("bold", 8)).place(x=35, y=70)
            predictnumLabel = Label(self.master, text="            ", width=10, font=("bold", 8)).place(x=100, y=70)
        width = 400
        height = 150
        try:
            self.img = Image.open(pathRoot + "\\projectTest\\BooksCover\\" + filename[:-4] + ".Jpg")
            self.img = self.img.resize((width, height), Image.ANTIALIAS)
            self.photoImg = ImageTk.PhotoImage(self.img)
            panel = tk.Label(image=self.photoImg)
            panel.image = self.photoImg
            panel.place(x=600, y=25)
        except:
            self.img = Image.open(No_Image_Cover)
            self.img = self.img.resize((width, height), Image.ANTIALIAS)
            self.photoImg = ImageTk.PhotoImage(self.img)
            panel = tk.Label(image=self.photoImg)
            panel.image = self.photoImg
            panel.place(x=600, y=25)
        # No_Image_Cover

    #Displays the books on the screen
    def setBooksOnScreen(self, pathRoot, listofBooks, y, type,No_Image_Cover):
        x = 50
        counter = 0
        width = 100
        height = 100
        userRecommendedBooks = shuffle(listofBooks)
        books_cover = os.fsencode(pathRoot + "\\projectTest\\BooksCover")
        bookCoverList = []
        for book_cover in os.listdir(books_cover):
            bookCoverfilename = str(book_cover.title(), 'utf-8')
            bookCoverfilename = bookCoverfilename[:-4]
            for recommendedbook in userRecommendedBooks:
                if type == "predict":
                        bookCoverList.append([recommendedbook[0],recommendedbook[1]])
                else:
                        bookCoverList.append([recommendedbook[0] , -1])
        for book in bookCoverList:
            if counter < 7:
                counter += 1
                try:
                    self.img = Image.open(pathRoot + "\\projectTest\\BooksCover\\" + book[0][:-4] + ".Jpg")
                    self.img = self.img.resize((width, height), Image.ANTIALIAS)
                    self.photoImg = ImageTk.PhotoImage(self.img)
                    panel = tk.Button(image=self.photoImg)
                    panel.config(command=lambda bookname=book, path=pathRoot: self.BookDetails(bookname, path,type,No_Image_Cover))
                    panel.image = self.photoImg
                    panel.place(x=x, y=y)
                except:
                    self.img = Image.open(No_Image_Cover)
                    self.img = self.img.resize((width, height), Image.ANTIALIAS)
                    self.photoImg = ImageTk.PhotoImage(self.img)
                    panel = tk.Button(image=self.photoImg)
                    panel.config(command=lambda bookname=book, path=pathRoot: self.BookDetails(bookname, path,type,No_Image_Cover))
                    panel.image = self.photoImg
                    panel.place(x=x, y=y)
                # No_Image_Cover
            else:
                break
            x += 150