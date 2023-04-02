# L2T13 -CAPSTONE PROJECT.
# Author: Debby Naude.
# Compulsory Task - Create a Book Store program using both Python and SQL to
# manage the books in the book store.
# Source - thanks to stackoverflow.com for some answers and inspiration.
# Remarks: Issue1 - 20230402: Remove obsolete remarks and spaces.

# Import Libraries.
import sqlite3

#Include exception handling for initial connection and table creation.
# Create a database for the books.
try:
    db = sqlite3.connect('data/books_db')
    # Get a cursor object.
    cursor = db.cursor()

    # Check whether table exists before creating it.
    cursor.execute('''CREATE TABLE IF NOT EXISTS
        book_store(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)''')
    
    db.commit()
except Exception as e:
        db.rollback
        raise e
finally:
    #Close the connection to DB
    db.close()

#Open the data base connection again to run the book store system.
db = sqlite3.connect('data/books_db')
cursor = db.cursor()
    
# ** Function Section **

#Search Function
def search_book(title):
    book_found = cursor.execute('''SELECT * FROM book_store WHERE Title = ?''',(title,)).fetchall()
    tot_found = len(book_found)
    if tot_found < 1:
        tot_found = 0
        book_found = []
        return tot_found, book_found
        pass
    else:
        return tot_found, book_found
    pass

#Process multiple books with same title.
def multiple_books(books_found):
    num = 0
    n = 0
    id_no = 0
    tot_qty = books_found[0]
    books = books_found[1]
    #Print out the list of books and their details.
    print(f"\nThe Book has been found, the number of books with this title is: {tot_qty}\n")
            
    for n in range(0,tot_qty):
        num += 1
        ID = books[n][0]
        name = books[n][1]
        author = books[n][2]
        quantity = books[n][3]
        print(f"Book number: {num}")
        print(f"ID = {ID}" )
        print(f"Title = {name}")
        print(f"Author = {author}")
        print(f"Quantity = {quantity}\n")
    id_no = input("Please select the ID number of the book details to updated: \n")
    books_found = cursor.execute('''SELECT * FROM book_store WHERE id = ?''',(id_no,)).fetchall()
    #Check if any records found with the ID number given.
    if len(books_found) == 0:
        print(f"ID number invalid {id_no}, please try again.\n")
        id_no = 0
        
    #Return the ID of the book record to be changed or deleted.
    return id_no
    pass

# Print function.
def print_books(tot_qty,books):
    num = 0
    n = 0
        
    #Print out the list of books and their details.            
    for n in range(0,tot_qty):
        num += 1
        ID = books[n][0]
        name = books[n][1]
        author = books[n][2]
        quantity = books[n][3]
        print(f"Book number: {num}")
        print(f"ID = {ID}" )
        print(f"Title = {name}")
        print(f"Author = {author}")
        print(f"Quantity = {quantity}\n")
    pass

# ** End Function Section **

#Update database with books already provided for the task.
book_list = [(3001,"A Tale of Two Cities","Charles Dickens", 30),(3002,"Harry Potter and the Philosepher's Stone","J.K. Rowling",40),\
             (3003,"The Lion, the Witch and the Wardrobe","C.S. Lewis",25),(3004,"The Lord of the Rings","J.R.R. Tolkien",37),\
             (3005,"Alice in Wonderland","Lewis Carroll",12)]

# Insert book record if it doesn't exist.
n = 0
while n < 5:
    id = book_list[n][0]
    id = int(id)
    #Check if record id already exists.
    cursor.execute('''SELECT * from book_store WHERE id = ?''',(id,))
    db_result = cursor.fetchall()
    #Insert records.
    if len(db_result) == 0:
        cursor.execute('''INSERT INTO book_store(id, Title, Author, Qty)
                  VALUES(?,?,?,?)''', (book_list[n]))
    n += 1
# Database updated.    
db.commit()


# ** Menu Section **
end = True

# List menu options.
while end:
    menu = input('''    ** WELCOME TO BOOKWORM BOOK STORE **\n 
    Please select one of the following options:\n 
    1. Enter a book title to add a book.
    2. Update book details.
    3. Delete a book.
    4. Search for a book.
    5. Print a report on all books.
    0. Exit.
    :''')

    ### Option 1 - Add a book.
    if menu == '1':
        tot_qty = 0
        title = ""
        #Enter book title to be added.
        title = input("Please enter the title of the book to be added: \n")
        #Check input not blank.
        if len(title) == 0:
            print("No title given, please try again.\n")
            pass
        else:
            #first use search function to check whether the book already exists in the database.
            books_found = search_book(title)
            tot_qty = books_found[0]
            books = books_found[1]
        
        #No books with the title found, add the book.
        if tot_qty < 1:
            if len(title) > 0:
                author = input("Please enter the author: \n")
                if len(author) == 0:
                    print("No author given, please try again.\n")
                    break
                try:
                    quantity = int(input("Please enter the quantity:\n"))
                    cursor.execute('''INSERT INTO book_store(Title, Author, Qty)
                    VALUES(?,?,?)''', (title, author, quantity))
                    print("Book added.\n")
                    db.commit()
                    
                except ValueError:
                    print("Invalid entry type, must be a number, please try again. \n")
                pass
                
        #If more than one book with the same title, check for the author.    
        elif tot_qty > 0:
            #Check if the same author.
            count = 0
            new_author = input("Title already on the system, please enter author for the new book:\n")
            cursor.execute('''SELECT COUNT() FROM book_store WHERE Author = ?
            AND Title = ?''',(new_author,title,))
            db_result = cursor.fetchone() 
            count = db_result[0]
            
            #Add the book if the author is different.
            if count == 0:
                quantity = input("Please enter the quantity:\n")
                cursor.execute('''INSERT INTO book_store(Title, Author, Qty)
                VALUES(?,?,?)''', (title, new_author, quantity))
                db.commit()
                print("Book added.\n")
            else:
                print("Book already exists, please try again.\n")
                pass
                  
        pass

    ### Option 2 - Update book details.    
    elif menu == '2':
        id_no = 0
        change = True
        #Enter book to be updated.
        title = input("Please enter the title of the book to be updated: \n")

        #Use search function to check whether the book is in the database.
        books_found = search_book(title)
        books = books_found[1]
        tot_qty = books_found[0]
        
        #If more than one book with the title, request the ID of the book to be updated.
        if tot_qty > 1:
            id_no = multiple_books(books_found)
            #Check if invalid ID given bypassed change.
            if id_no == 0:
                change = False
                pass
            
        #One book found with the title.
        elif tot_qty == 1:
            id_no = books[0][0]
            
        #No books found with the title.
        else:
            print(f"No books found with the title {title}.\n")
            change = False
            pass
                     
        #Change the record.
        if change:
            #Redo the select statement to get the selected record from the records with the same book title.
            cursor.execute('''SELECT * FROM book_store WHERE id = ?''',(id_no,))
            db_result = cursor.fetchone()
            ID = db_result[0]
            name = db_result[1]
            author = db_result[2]
            quantity = db_result[3]
        while change:
            choice = input('''Please select the number of the field you would like to change:
                1 - Title
                2 - Author
                3 - Quantity
                4 - Exit
                :''')

            #Change title.
            if choice == '1':
                new_title = input(f"Current Title is {name}, please enter the new title: \n")
                if len(new_title) > 0:
                    cursor.execute('''UPDATE book_store SET Title = ?
                        WHERE id = ?''',(new_title,ID,))
                    print(f"Title updated to {new_title}\n")
                    db.commit()
                    name = new_title
                else:
                    print("No title given, please try again.\n")
                    pass

            #Change author.
            elif choice == '2':
                new_author = input(f"Current Author is {author}, please enter the new title: \n")
                if len(new_author) > 0:
                    cursor.execute('''UPDATE book_store SET Author = ?
                        WHERE id = ?''',(new_author,ID,))
                    print(f"Author updated to {new_author}\n")
                    db.commit()
                    author = new_author
                else:
                    print("No author given, please try again.\n")
                    pass
                
            #Change quantity.
            elif choice == '3':
                try:
                    new_quantity = int(input(f"Current Quantity is {quantity}, please enter the new quantity: \n"))
                    cursor.execute('''UPDATE book_store SET Qty = ?
                        WHERE id = ?''',(new_quantity,ID,))
                    print(f"Quantity updated to {new_quantity}\n")
                    db.commit()
                    quantity = new_quantity
                #Non numeric entry.   
                except ValueError:
                       print("Invalid entry type, must be a number, please try again. \n")
                       pass
                
            #Exit.
            elif choice == '4':
                change = False
                pass

            #Invalid choice.
            else:
                print(f"Invalid choice: {choice}, please try again.\n")
                change = False
                pass
        pass

    ### Option 3 - Delete a book.
    elif menu == '3':
        title = ""
        cont_del = "N"
        tot_qty = 0
        title = input("Please enter the title of the book to be deleted: \n")
        #Check if no title entered.
        if len(title) == 0:
            pass
        #Use search function to check whether the book is in the database.
        else:
            books_found = search_book(title)
            books = books_found[1]
            tot_qty = books_found[0]
        
        #If more than one book with the title, request the ID of the book to be updated.
        if tot_qty > 1:
            id_no = multiple_books(books_found)
            #Invalid ID given.
            if id_no == 0:
                pass
            else:
                cont_del = "Y"
        elif tot_qty == 1:
            id_no = books[0][0]
            cont_del = "Y"
        else:
            print(f"Book with the title {title} or blank, not found, please try again.\n")
            pass
        
        #Request final confirmation before deleting the record.
        if cont_del == "Y":
            #Confirm the book to be deleted giving title and author.
            cursor.execute('''SELECT * FROM book_store WHERE id = ?''',(id_no,))
            db_result = cursor.fetchone()
            title = db_result[1]
            author = db_result[2]
            print(f"Book {title}, by author {author}, will now be deleted.\n")
            confirm = input("Please confirm Y or N : ")
            #Complete the deletion or exit the option.
            if confirm.upper() == "Y":
                cursor.execute('''DELETE FROM book_store WHERE id = ?''',(id_no,))
                print(f"Book {title}, by author {author}, deleted from the system\n")
                db.commit()
            else:
                print(f"{title} delete request has been cancelled.\n")
        pass

    ### Option 4 - Search for a book by title and print its details.
    elif menu == '4':
        title = input("Please enter the title of the book to be found: \n")
        books = []
        #execute function to search for a book.
        books_found = search_book(title)
        books = books_found[1]
        tot_qty = books_found[0]
        #Check if any books found and print list if found.
        if tot_qty > 0:
            print(f"Book {title}, found, printing details: \n")
            print_books(tot_qty,books)
        else:            
            print(f"Book {title}, not found, please try again\n")
        pass

    ### Option 5 - Print all records in the table book_store.
    elif menu == '5':
        books = cursor.execute('''SELECT * FROM book_store''').fetchall()
        tot_qty = len(books)
        if tot_qty == 0:
            print("No books in the book_store database, please add books first.\n")
            pass
        else:
            print(f"The number of books found in the system is: {tot_qty}\n")
            print_books(tot_qty,books)
            pass
            
    ### Exit Menu.    
    elif menu == '0':
        db.close()
        print("Goodbye\n")
        break
    else:
        print("Menu option incorrect, please try again.\n")
        pass
        
        

    


