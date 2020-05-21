import mysql.connector

# Connection to database
mydb = mysql.connector.connect(
     host="<your host name>", # "localhost"
     database='database',
     user="<your user name>", # "root"
     passwd="<your MySQL workbanch Password>",
     buffered=True
 
)


# MySQL queries class
class MySQL:
    # Send a user login statement on the system
    # A function that accepts two parameters id and password
    # True Shows that the process went through successfully
    # False is a situation where one of the fields is incorrect
    def login(self, id, password):
        print("MySQL Class - iMessage_login")
        cursor = mydb.cursor()
        sql = "SELECT `user`.`password` FROM `database`.`user` WHERE user_id =%s ;"
        userId = (id,)
        try:
            cursor.execute(sql, userId)
            mydb.commit()
            userPassword = cursor.fetchone()[0]
            if (userPassword == False):
                return (False)
            elif (userPassword == password):
                return (True)
        except:
            return (False)

    # gets a user id and retrieves his reading history
    def getbook(self, id):
        cursor = mydb.cursor()
        sql = "SELECT `bookinusers`.`FileName`,`bookinusers`.`Rating` " \
              " FROM `database`.`bookinusers` WHERE `User Id` = %s;"
        val = (id,)
        try:
            cursor.execute(sql, val)
            mydb.commit()
            myresult = cursor.fetchall()
            sample = []
            for result in myresult:
                sample.append(result)
            return (sample)
        except:
            return (False)

    # gets a book filename and retrieves the book title and book's author
    def getAuthor(self, filename):
        cursor = mydb.cursor()
        sql = "SELECT `book`.`Title`,`book`.`Author` FROM `database`.`book` WHERE FileName =%s ;"
        val = (filename,)
        try:
            cursor.execute(sql, val)
            mydb.commit()
            result = cursor.fetchall()
            TitleAndAuthor = []
            for vector in result:
                TitleAndAuthor.append(vector[0])
                TitleAndAuthor.append(vector[1])
            return (TitleAndAuthor)
        except:
            return (False)

    # retrieves a list of all books features from database
    def getAllBooksFeatures(self):
        cursor = mydb.cursor()
        sql = "SELECT `book`.`FileName`,`book`.`FeautureVec` FROM `database`.`book`  ;"

        try:
            cursor.execute(sql)
            mydb.commit()
            result = cursor.fetchall()
            filenameAndFeatures = []
            for vector in result:
                filenameAndFeatures.append(vector)
            return (filenameAndFeatures)
        except:
            return (False)

    # retrieves a list of all books filenames from database
    def getAllBooks(self):
        cursor = mydb.cursor()
        sql = "SELECT `book`.`FileName` FROM `database`.`book`  ;"
        try:
            cursor.execute(sql)
            mydb.commit()
            result = cursor.fetchall()
            filename = []
            for vector in result:
                filename.append(vector)
            return (filename)
        except:
            return (False)

    # gets a user id and retrieves a list of all relevant data of his reading history
    def getUserBooksFeatures(self, id):
        cursor = mydb.cursor()
        sql = "SELECT `book`.`FileName`, `book`.`FeautureVec`,`bookinusers`.`Rating` " \
              "FROM `database`.`book`,`database`.`bookinusers` " \
              "where `bookinusers`.`User Id` = %s and `book`.`FileName`=`bookinusers`.`FileName` ;"
        val = (id,)
        try:
            cursor.execute(sql, val)
            mydb.commit()
            result = cursor.fetchall()
            filenameAndFeatures = []
            for vector in result:
                filenameAndFeatures.append(vector)
            return (filenameAndFeatures)
        except:
            return (False)

    # retrieves pointer to the last row in [user,book] join table
    def GetTheLastIdInBookInUser(self):
        cursor = mydb.cursor()
        sql = " SELECT `bookinusers`.`IdUserBook` " \
              "FROM `database`.`bookinusers` " \
              "WHERE `bookinusers`.`IdUserBook`=(SELECT MAX(`bookinusers`.`IdUserBook`) " \
              "FROM `database`.`bookinusers`);"

        try:
            cursor.execute(sql)
            mydb.commit()
            result = cursor.fetchone()[0]
            return (result)
        except:
            return (False)

    # inserts/updates a new book data to the user reading history
    def InsertNewBookToUserReadingHistory(self, bookname, id, rating, IdUserInBook):
        cursor = mydb.cursor()
        sql = "SELECT `bookinusers`.`IdUserBook` FROM `database`.`bookinusers` " \
              "where `bookinusers`.`User Id` = %s  and `bookinusers`.`FileName` = %s;"
        val = (str(id), str(bookname))
        try:
            cursor.execute(sql, val)
            mydb.commit()
            result = cursor.fetchone()[0]
            sql = "UPDATE `database`.`bookinusers` " \
                  "SET `bookinusers`.`Rating` = %s " \
                  "WHERE `bookinusers`.`IdUserBook` = %s and `bookinusers`.`User Id`=%s and" \
                  " `bookinusers`.`FileName`= %s ;"
            val = (str(rating), str(result), str(id), str(bookname))
            cursor.execute(sql, val)
            mydb.commit()
            return (True)
        except:
            sql = "INSERT INTO `database`.`bookinusers`(`bookinusers`.`IdUserBook`,`bookinusers`.`User Id`,`bookinusers`.`Rating`,`bookinusers`.`FileName`)" \
                  "VALUES (%s, %s, %s, %s);"
            IdUserInBook += 1
            val = (str(IdUserInBook), str(id), str(rating), str(bookname))
            cursor.execute(sql, val)
            mydb.commit()
            return (True)

    # gets book title and retrieves the book filename
    def getFileName(self, Title):
        cursor = mydb.cursor()
        sql = "SELECT `book`.`FileName` " \
              "FROM `database`.`book` " \
              "where `book`.`Title` = %s ;"
        val = (Title,)
        try:
            cursor.execute(sql, val)
            mydb.commit()
            result = cursor.fetchone()[0]
            return (result)
        except:
            return (False)

    # gets text and retrieves anything that match to this text(books,author)
    def SearchBook(self, searchtext):
        cursor = mydb.cursor()
        sql = "SELECT `book`.`Title`, `book`.`FileName`, `Author` FROM `database`.`book` WHERE MATCH (`book`.`Title`, `book`.`Author`) AGAINST (%s);"
        val = (searchtext,)
        try:
            cursor.execute(sql, val)
            mydb.commit()
            result = cursor.fetchall()
            TitleFilenameAuthor = []
            for vector in result:
                TitleFilenameAuthor.append(vector)
            return (TitleFilenameAuthor)
        except:
            return (False)