import typer
import database
from rich.console import Console
from rich.table import Table
from typing import Optional

console = Console()

app = typer.Typer()

curr_user = None

@app.command("start")
def start():
    typer.echo(f"Welcome to Library CLI!")
    typer.echo(f"You can execute command '--help' to see the possible commands")
    database.connect()

@app.command("sign_up")
def sign_up(username: str):
    typer.echo(f"Nice that you are signing up!")
    usernames = database.get_usernames()
    while username in usernames:
        print("This username already exists!")
        username = input("Please enter another username: ")
    password = input("Please enter your password: ")
    database.add_user(username, password)
    global curr_user
    curr_user = username
    print("Successfully signed up!")

@app.command("sign_in")
def sign_in(username: str):
    usernames = database.get_usernames()
    if username in usernames:
        print("This username doesn't exist. Please sign up!")
        return
    typer.echo(f"Let's sign in!")
    correct_password = database.get_password(username)
    password = input("Please enter your password: ")
    while correct_password != password:
        print("Wrong password! Please enter again: ")
    global curr_user
    curr_user = username
    print("Successfully signed in!")

@app.command("add_book")
def add_book():
    typer.echo(f"Please enter the required book info to add!")
    name = input("Name: ")
    author = input("Author: ")
    page = input("# Pages: ")
    genre = input("Genre: ")
    database.add_book(name, author, page, genre)
    typer.echo(f"Book successfully added!")

@app.command("search_by_name")
def search_by_name(name: str):
    books = database.search_book_by_name(name)
    display_book_table(books)

@app.command("search_by_author")
def search_by_author(author: str):
    books = database.search_book_by_author(author)
    display_book_table(books)

@app.command("most_read_books")
def most_read_books(genre: Optional[str] = typer.Argument(None)):
    if genre is None:
        books = database.most_read_books()
    else:
        books = database.most_read_books_by_genre(genre)
    display_book_table(books)

@app.command("most_read_authors")
def most_read_authors(genre: Optional[str] = typer.Argument(None)):
    if genre is None:
        books = database.most_read_authors()
    else:
        books = database.most_read_authors_by_genre(genre)
    display_book_table(books)

@app.command("most_favorite")
def most_favorite(genre: Optional[str] = typer.Argument(None)):
    if genre is None:
        books = database.most_favorite()
    else:
        books = database.most_favorite_by_genre(genre)
    display_book_table(books)

@app.command("added_recently")
def most_read(genre: Optional[str] = typer.Argument(None)):
    if genre is None:
        books = database.get_recent_books()
    else:
        books = database.get_recent_books_by_genre(genre)
    display_book_table(books)

@app.command("most_read_genres")
def most_read_genres():
    most_read_genres = database.most_read_genres()
    print("Most read 5 genres:", most_read_genres)

@app.command("borrow_book")
def borrow_book(book_id: str):
    # get book availability
    available = database.is_book_available(book_id)
    if available:
        database.borrow_book(curr_user, book_id)
        typer.echo("You borrowed book " + book_id)
    else:
        typer.echo(f"Sorry, this book is not available! Try again later.")

@app.command("return_book")
def return_book(book_id: str):
    borrowed = database.is_borrowed(curr_user, book_id)
    if not borrowed:
        typer.echo("Sorry, you didn't borrow book " + book_id)
    else:
        database.return_book(curr_user, book_id)
        typer.echo("You returned book " + book_id)

@app.command("mark_read")
def mark_read(book_id: str):
    database.mark_read(curr_user, book_id)
    print("You marked book", book_id, "as read")

@app.command("mark_reading")
def mark_reading(book_id: str):
    database.mark_reading(curr_user, book_id)
    print("You marked book", book_id, "as reading")

@app.command("mark_will_read")
def mark_will_read(book_id: str):
    database.mark_will_read(curr_user, book_id)
    print("You marked book", book_id, "as will read")

@app.command("fav_book")
def fav_book(book_id: str):
    database.add_fav(curr_user, book_id)
    print("You added book", book_id, "to your favorites")

@app.command("my_books")
def my_books():
    read_books = database.get_books_read(curr_user)
    typer.echo(f"Books you read:")
    display_book_table(read_books)
    reading_books = database.get_books_reading(curr_user)
    typer.echo(f"Books you are reading:")
    display_book_table(reading_books)
    will_read_books = database.get_books_will_read(curr_user)
    typer.echo(f"Books you will read:")
    display_book_table(will_read_books)

@app.command("statistics")
def statistics():
    read_books = database.get_books_read(curr_user)
    typer.echo(f"Number of books you read: " + read_books.size())

def display_book_table(books):
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=10)
    table.add_column("Book ID", style="dim", min_width=10, justify=True)
    table.add_column("Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("# Pages", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)

    for idx, book in enumerate(books, start=1):
        table.add_row(str(idx), str(book[0]), book[1], book[2], str(book[3]), book[4], book[5])

    console.print(table)

if __name__ == "__main__":
    app()
