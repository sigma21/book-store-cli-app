import typer
import database
from rich.console import Console
from rich.table import Table
from typing import Optional

console = Console()

app = typer.Typer()

@app.command("start")
def start():
    typer.echo(f"Welcome to Library CLI!")
    typer.echo(f"You can execute command '--help' to see the possible commands")
    database.connect()

@app.command("sign_up")
def sign_up(username: str):
    typer.echo(f"Nice that you are signing up!")
    usernames = database.get_users()
    while username in usernames:
        print("This username already exists!")
        username = input("Please enter another username: ")
    username = input("Please enter your password: ")
    database.add_user(username, password)
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

@app.command("search_by_author")
def search_by_author(author: str):
    books = database.search_book_by_author(author)
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

@app.command("most_read")
def most_read(genre: Optional[str] = typer.Argument(None)):
    if genre is None:
        most_read_10 = database.most_read_10()
    else:
        most_read_10_genre = database.most_read_10_by_genre(genre)

@app.command("most_read_genres")
def most_read_genres():
    most_read_5_genres = database.most_read_genres()
    typer.echo(f"Most read 5 genres: ")

@app.command("borrow_book")
def borrow_book(book_id: str):
    # get book availability
    available = database.is_book_available(book_id)
    if available:
        database.borrow_book(book_id)
        typer.echo("You borrowed book " + book_id)
    else:
        typer.echo(f"Sorry, this book is not available! Try again later.")

@app.command("return_book")
def return_book(book_id: str):
    borrowed = database.is_borrowed(book_id)
    if not borrowed:
        typer.echo("Sorry, you didn't borrow book " + book_id)
    else:
        database.return_book(book_id)
        typer.echo("You returned book " + book_id)

if __name__ == "__main__":
    app()
