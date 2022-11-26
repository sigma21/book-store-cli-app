import psycopg2

def connect():
    conn = None
    try:
        try:
            # try to connect to database
            conn = psycopg2.connect(
                host="localhost",
                database="bookstore",
                user="postgres",
                password="postgres")
        except (Exception, psycopg2.DatabaseError) as error:
            # if database doesn't exist, create it
            conn = psycopg2.connect(
                host="localhost",
                database="bookstore",
                user="postgres",
                password="postgres")
            conn.autocommit = True
            curr = conn.cursor()
            curr.execute("CREATE DATABASE bookstore")
            curr.close() 
            conn = psycopg2.connect(
                host="localhost",
                database="bookstore",
                user="postgres",
                password="postgres")

        conn.autocommit = True
        curr = conn.cursor()
        # check which tables we have
        curr.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        table_names = curr.fetchall()
        # if there are no tables create them
        if len(table_names) == 0:
            file = open('bookstore.sql', 'r')
            sqlFile = file.read()
            file.close()
            # all SQL commands (split on ';')
            sqlCommands = sqlFile.split(';')[:-1]
            # Execute every command from the input file
            for command in sqlCommands:
                try:
                    curr.execute(command)
                except (Exception, psycopg2.DatabaseError) as error:
                    break
            curr.close()  

    except (Exception, psycopg2.DatabaseError) as error:
        print("Please start PostgreSQL server in your computer to connect to Library DB!")      
    finally: 
        if conn is not None:
            conn.close()

def get_users():
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute('SELECT username FROM public."Users"')
    users = curr.fetchall()
    usernames = []
    for user in users:
        usernames.append(user[0])
    curr.close()
    conn.close()
    return usernames

def add_user(user, password):
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute(f'INSERT INTO public."Users"(username, password) VALUES (\'{user}\', \'{password}\')')
    curr.close()
    conn.close()

def search_book_by_name(name):
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM public."Book" WHERE name = \'{name}\'')
    books = curr.fetchall()
    curr.close()
    conn.close()
    return books

def search_book_by_author(author):
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM public."Book" WHERE author = \'{author}\'')
    books = curr.fetchall()
    curr.close()
    conn.close()
    return books

def search_book_by_name_and_author(name, author):
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM public."Book" WHERE name = \'{name}\' and author = \'{author}\'')
    books = curr.fetchall()
    curr.close()
    conn.close()
    return books

def get_book_by_id(id):
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute(f'SELECT * FROM public."Book" WHERE id = {id}')
    book = curr.fetchone()
    curr.close()
    conn.close()
    return book

def get_books():
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute('SELECT * FROM public."Book"')
    books = curr.fetchall()
    curr.close()
    conn.close()
    return books

def get_recent_books():
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute('SELECT * FROM public."Book" SORT BY date_added DESC LIMIT 10')
    books = curr.fetchall()
    curr.close()
    conn.close()
    return books

def add_book(name, author, page, genre):
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    existing = search_book_by_name_and_author(name, author)
    if len(existing) == 0:
        curr.execute(f'''INSERT INTO public."Book"(name, author, page, genre, available_quantity, total_quantity) 
            VALUES (\'{name}\', \'{author}\', {int(page)}, \'{genre}\', 1, 1)''')
    else:
        curr.execute(f'''INSERT INTO public."Book"(name, author, page, genre, available_quantity, total_quantity) 
            VALUES (\'{name}\', \'{author}\', {int(page)}, \'{genre}\', {existing[0][4] + 1}, {existing[0][5] + 1})''')
    curr.close()
    conn.close()

def borrow_book(id):
    conn = psycopg2.connect(
            host="localhost",
            database="bookstore",
            user="postgres",
            password="postgres")
    conn.autocommit = True
    curr = conn.cursor()
    book = get_book_by_id(id)
    curr.execute(f'''UPDATE public."Book" SET available_quantity = {book[4]}, total_quantity = {book[5]}
        WHERE id = {id})''')
