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

def get_books():
    cur = connect()
    cur.execute('SELECT * FROM public."Book"')
    books = cur.fetchall()
    return books

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
        cur.execute(f'''INSERT INTO public."Book"(name, author, page, genre, available_quantity, total_quantity) 
            VALUES (\'{name}\', \'{author}\', {page}, \'{genre}\', 1, 1)''')
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
    print(username)
    cur.execute(f'UPDATE public."Book" SET available_quantity = {int(book[5]) - 1} WHERE book_id = {book_id}')
    user_book = search_user_book(username, book_id)
    if user_book is None:
        cur.execute(f'INSERT INTO public."User_Book"(book_id, username) VALUES (\'{book_id}\', \'{username}\')')
    else:
        cur.execute(f'UPDATE public."User_Book" SET borrowed_amount = {user_book[5] + 1} WHERE id = {user_book[0]})')

def return_book(username, book_id):
    cur = connect()
    book = get_book_by_id(book_id)
    cur.execute(f'UPDATE public."Book" SET available_quantity = {int(book[5]) + 1} WHERE book_id = {book_id})')
    # add info that this user returned this book

def is_book_available(book_id):
    cur = connect()
    cur.execute(f'SELECT * FROM public."Book" WHERE book_id = {book_id} AND available_quantity > 0')
    available_books = cur.fetchall()
    return len(available_books) > 0

def most_read_books():
    cur = connect()
    cur.execute(f'SELECT book_id, count(*) as count FROM public."User_Book" WHERE reading_status = \'read\' GROUP BY book_id, username ORDER BY count DESC LIMIT 10')
    most_read_books = cur.fetchall()
    most_read_book_ids = list(zip(*most_read_books))[0]
    return most_read_book_ids

def most_read_books_by_genre(genre):
    cur = connect()
    cur.execute(f'''SELECT book_id, count(*) as count FROM public."User_Book" INNER JOIN public."Book" ON book_id WHERE reading_status = \'read\' 
        AND genre = \'{genre}\' GROUP BY book_id, username ORDER BY count DESC LIMIT 10''')
    most_read_books = cur.fetchall()
    most_read_book_ids = list(zip(*most_read_books))[0]
    return most_read_book_ids

def most_read_genres():
    cur = connect()
    cur.execute(f'''SELECT genre, count(*) as count FROM public."User_Book" INNER JOIN public."Book" ON book_id WHERE reading_status = read 
        GROUP BY book_id, username, genre ORDER BY count DESC LIMIT 10''')
    most_read = cur.fetchall()
    most_read_genres = list(zip(*most_read))[0]
    return most_read_genres