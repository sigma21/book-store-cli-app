import psycopg2

def connect():
    conn = None
    try:
        try:
            # try to connect to database
            conn = psycopg2.connect(
                host="localhost",
                database="library",
                user="postgres",
                password="postgres")
        except (Exception, psycopg2.DatabaseError) as error:
            # if database doesn't exist, create it
            conn = psycopg2.connect(
                host="localhost",
                database="library",
                user="postgres",
                password="postgres")
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("CREATE DATABASE library")
             
            conn = psycopg2.connect(
                host="localhost",
                database="library",
                user="postgres",
                password="postgres")

        conn.autocommit = True
        cur = conn.cursor()
        # check which tables we have
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        table_names = cur.fetchall()
        # if there are no tables create them
        if len(table_names) == 0:
            file = open('library.sql', 'r')
            sqlFile = file.read()
            file.close()
            # all SQL commands (split on ';')
            sqlCommands = sqlFile.split(';')[:-1]
            # Execute every command from the input file
            for command in sqlCommands:
                try:
                    cur.execute(command)
                except (Exception, psycopg2.DatabaseError) as error:
                    break
        return cur

    except (Exception, psycopg2.DatabaseError) as error:
        print("Please start PostgreSQL server in your computer to connect to Library DB!")
        print(error)      

def get_usernames():
    cur = connect()
    cur.execute('SELECT username FROM public."Users"')
    users = cur.fetchall()
    usernames = []
    for user in users:
        usernames.append(user[0])
    return usernames

def add_user(username):
    cur = connect()
    cur.execute(f'INSERT INTO public."Users"(username) VALUES (\'{username}\')')

def search_book_by_name(name):
    cur = connect()
    cur.execute(f'SELECT * FROM public."Book" WHERE name = \'{name}\'')
    books = cur.fetchall()
    return books

def search_book_by_author(author):
    cur = connect()
    cur.execute(f'SELECT * FROM public."Book" WHERE author = \'{author}\'')
    books = cur.fetchall()
    return books

def search_book_by_name_and_author(name, author):
    cur = connect()
    cur.execute(f'SELECT * FROM public."Book" WHERE name = \'{name}\' and author = \'{author}\'')
    books = cur.fetchall()
    return books

def get_book_by_id(book_id):
    cur = connect()
    cur.execute(f'SELECT * FROM public."Book" WHERE book_id = {book_id}')
    book = cur.fetchone()
    return book

def get_recent_books():
    cur = connect()
    cur.execute('SELECT * FROM public."Book" ORDER BY date_added DESC LIMIT 5')
    books = cur.fetchall()
    return books

def get_recent_books_by_genre(genre):
    cur = connect()
    cur.execute(f'SELECT * FROM public."Book" WHERE genre = \'{genre}\' ORDER BY date_added DESC LIMIT 5')
    books = cur.fetchall()
    return books

def add_book(name, author, page, genre):
    cur = connect()
    existing = search_book_by_name_and_author(name, author)
    if len(existing) == 0:
        cur.execute(f'''INSERT INTO public."Book"(name, author, page, genre) 
            VALUES (\'{name}\', \'{author}\', {page}, \'{genre}\')''')
    else:
        cur.execute(f'''UPDATE public."Book" SET available_quantity = {int(existing[0][5]) + 1},
            total_quantity = {int(existing[0][6]) + 1} WHERE book_id = {int(existing[0][0])}''')

def search_user_book(username, book_id):
    cur = connect()
    cur.execute(f'SELECT * FROM public."User_Book" WHERE username = \'{username}\' and book_id = \'{book_id}\'')
    user_book = cur.fetchall()
    if len(user_book) > 0:
        return user_book[0]
    else:
        return None

def borrow_book(username, book_id):
    cur = connect()
    book = get_book_by_id(book_id)
    cur.execute(f'UPDATE public."Book" SET available_quantity = {int(book[5]) - 1} WHERE book_id = {book_id}')
    user_book = search_user_book(username, book_id)
    if user_book is None:
        cur.execute(f'INSERT INTO public."User_Book"(book_id, username, borrowed_amount) VALUES (\'{book_id}\', \'{username}\', 1)')
    else:
        cur.execute(f'UPDATE public."User_Book" SET borrowed_amount = {user_book[5] + 1} WHERE id = {user_book[0]})')
    
def return_book(username, book_id):
    cur = connect()
    book = get_book_by_id(book_id)
    cur.execute(f'UPDATE public."Book" SET available_quantity = {int(book[5]) + 1} WHERE book_id = {book_id}')
    user_book = search_user_book(username, book_id)
    cur.execute(f'UPDATE public."User_Book" SET borrowed_amount = {user_book[5] - 1} WHERE id = {user_book[0]}')

def is_book_available(book_id):
    cur = connect()
    cur.execute(f'SELECT * FROM public."Book" WHERE book_id = {book_id} AND available_quantity > 0')
    available_books = cur.fetchall()
    return len(available_books) > 0

def is_borrowed(username, book_id):
    cur = connect()
    cur.execute(f'SELECT * FROM public."User_Book" WHERE book_id = {book_id} AND username = \'{username}\' AND borrowed_amount > 0')
    borrowed_books = cur.fetchall()
    return len(borrowed_books) > 0

def mark_status(username, book_id, status):
    cur = connect()
    user_book = search_user_book(username, book_id)
    if user_book is None:
        cur.execute(f'INSERT INTO public."User_Book"(book_id, username, reading_status) VALUES (\'{book_id}\', \'{username}\', \'{status}\')')
    else:
        cur.execute(f'UPDATE public."User_Book" SET reading_status = \'{status}\' WHERE book_id = {book_id} AND username = \'{username}\'')

def add_fav(username, book_id):
    cur = connect()
    user_book = search_user_book(username, book_id)
    if user_book is None:
        cur.execute(f'INSERT INTO public."User_Book"(book_id, username, is_fav) VALUES (\'{book_id}\', \'{username}\', true)')
    else:
        cur.execute(f'UPDATE public."User_Book" SET is_fav = true WHERE id = {user_book[0]}')
        
def get_books_with_status(username, status):
    cur = connect()
    cur.execute(f'SELECT book_id FROM public."User_Book" WHERE username = \'{username}\' AND reading_status = \'{status}\'')
    book_ids = cur.fetchall()
    books = get_books_by_ids(book_ids)
    return books

def get_fav_books(username):
    cur = connect()
    cur.execute(f'SELECT book_id FROM public."User_Book" WHERE username = \'{username}\' AND is_fav is true')
    book_ids = cur.fetchall()
    books = get_books_by_ids(book_ids)
    return books

def get_books_by_ids(ids):
    cur = connect()
    books = []
    for id in ids:
        cur.execute(f'SELECT * FROM public."Book" WHERE book_id = {int(id[0])}')
        book = cur.fetchone() 
        books.append(book)
    return books

def most_read_books():
    cur = connect()
    cur.execute(f'SELECT book_id, count(*) as count FROM public."User_Book" WHERE reading_status = \'read\' GROUP BY book_id, username ORDER BY count DESC LIMIT 10')
    most_read_books = cur.fetchall()
    books = get_books_by_ids(most_read_books)
    return books

def most_read_books_by_genre(genre):
    cur = connect()
    cur.execute(f'''SELECT book.book_id, count(*) as count FROM public."User_Book" as user_book INNER JOIN public."Book" as book ON user_book.book_id = book.book_id WHERE reading_status = \'read\' 
        AND genre = \'{genre}\' GROUP BY book.book_id, user_book.username ORDER BY count DESC LIMIT 10''')
    most_read_books = cur.fetchall()
    books = get_books_by_ids(most_read_books)
    return books

def most_favorite():
    cur = connect()
    cur.execute(f'SELECT book_id, count(*) as count FROM public."User_Book" WHERE is_fav IS true GROUP BY book_id, username ORDER BY count DESC LIMIT 10')
    most_fav_books = cur.fetchall()
    books = get_books_by_ids(most_fav_books)
    return books

def most_favorite_by_genre(genre):
    cur = connect()
    cur.execute(f'''SELECT book.book_id, count(*) as count FROM public."User_Book" as user_book INNER JOIN public."Book" as book ON user_book.book_id = book.book_id WHERE is_fav IS true 
        AND genre = \'{genre}\' GROUP BY book.book_id, user_book.username ORDER BY count DESC LIMIT 10''')
    most_fav_books = cur.fetchall()
    books = get_books_by_ids(most_fav_books)
    return books

def most_read_genres():
    cur = connect()
    cur.execute(f'''SELECT book.genre, count(*) as count FROM public."User_Book" as user_book INNER JOIN public."Book" as book ON user_book.book_id = book.book_id WHERE user_book.reading_status = \'read\' 
        GROUP BY user_book.book_id, user_book.username, book.genre ORDER BY count DESC LIMIT 5''')
    most_read = cur.fetchall()
    most_read_genres = []
    for genre in most_read:
        most_read_genres.append(genre[0])
    return most_read_genres

def most_read_authors():
    cur = connect()
    cur.execute(f'''SELECT book.author, count(*) as count FROM public."User_Book" as user_book INNER JOIN public."Book" as book ON user_book.book_id = book.book_id WHERE user_book.reading_status = \'read\' 
        GROUP BY user_book.book_id, user_book.username, book.author ORDER BY count DESC LIMIT 3''')
    most_read = cur.fetchall()
    most_read_authors = []
    for author in most_read:
        most_read_authors.append(author[0])
    return most_read_authors

def get_statistics(username):
    cur = connect()
    cur.execute(f'''WITH read_books_by_user AS (SELECT DISTINCT book.book_id AS book_id FROM public."User_Book" as user_book INNER JOIN public."Book" as book ON user_book.book_id = book.book_id WHERE 
        user_book.reading_status = \'read\' AND username = \'{username}\') SELECT COUNT(*) FROM read_books_by_user''')
    number_of_books = cur.fetchone()[0]
    cur.execute(f'''WITH read_books_by_user AS (SELECT DISTINCT book.author AS author FROM public."User_Book" as user_book INNER JOIN public."Book" as book ON user_book.book_id = book.book_id WHERE 
        user_book.reading_status = \'read\' AND username = \'{username}\') SELECT COUNT(*) FROM read_books_by_user''')
    number_of_authors = cur.fetchone()[0]
    cur.execute(f'''WITH read_books_by_user AS (SELECT DISTINCT book.genre AS genre FROM public."User_Book" as user_book INNER JOIN public."Book" as book ON user_book.book_id = book.book_id WHERE 
        user_book.reading_status = \'read\' AND username = \'{username}\') SELECT COUNT(*) FROM read_books_by_user''')    
    number_of_genres = cur.fetchone()[0]
    cur.execute(f'''WITH read_books_by_user AS (SELECT book.page AS page FROM public."User_Book" as user_book INNER JOIN public."Book" as book ON user_book.book_id = book.book_id WHERE 
        user_book.reading_status = \'read\' AND username = \'{username}\') SELECT SUM(page) FROM read_books_by_user''')  
    total_pages = cur.fetchone()[0]
    return number_of_books, number_of_authors, number_of_genres, total_pages
